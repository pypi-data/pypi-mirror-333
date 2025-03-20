import ast
import csv
import glob
import logging
import os
import pickle
import shutil
import string
import time

import matplotlib.pyplot as plt
import pandas as pd
from dotenv import load_dotenv
from natsort import natsorted, realsorted
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from river import compose, drift
from river import feature_extraction as fx
from river import forest, metrics, naive_bayes, neighbors, stream, tree
from send2trash import send2trash

from online_news_classification import constants
from online_news_classification.functions import manage_datasets, setup

load_dotenv()


def get_key(fp):
    filename = os.path.splitext(os.path.basename(fp))[0]
    int_part = filename.split("_")[3]
    return int(int_part)


def extract_integer(filename):
    if filename.endswith(".csv"):
        return int(filename.split(".")[0].split("_")[1])
    else:
        return -1


def feature_extraction_model(args):
    if args.feature_extraction == "BoW":
        en_stops = set(stopwords.words("english"))
        feature_extraction = fx.BagOfWords(
            lowercase=True, strip_accents=False, on="text", stop_words=en_stops
        )
    else:
        feature_extraction = fx.TFIDF(lowercase=True, strip_accents=False, on="text")
    return feature_extraction


def classifier_model(args):
    classification_type = args.classification_type
    grace_period = float(os.getenv("GRACE_PERIOD"))
    delta = float(os.getenv("DELTA"))
    split_criterion = os.getenv("SPLIT_CRITERION")

    classifier_map = {
        "hdt_adaptive": tree.HoeffdingAdaptiveTreeClassifier(
            grace_period=grace_period,
            delta=delta,
            split_criterion=split_criterion,
            max_depth=1000,
            bootstrap_sampling=False,
            drift_detector=drift.binary.DDM(),
            nominal_attributes=["category"],
            seed=1,
        ),
        "hdt_non_adaptive": tree.HoeffdingTreeClassifier(
            grace_period=grace_period,
            delta=delta,
            split_criterion=split_criterion,
            max_depth=1000,
            nominal_attributes=["category"],
        ),
        "naive_bayes": naive_bayes.MultinomialNB(alpha=1),
        "forest_amf": forest.AMFClassifier(
            n_estimators=10, use_aggregation=True, dirichlet=0.5, seed=1
        ),
        "knn": neighbors.KNNClassifier(),
    }

    classifier = classifier_map.get(
        classification_type, classifier_map["hdt_non_adaptive"]
    )

    if classification_type not in classifier_map:
        logging.info(
            f"Warning: Unsupported classification type '{classification_type}'. "
            + "Using default classifier."
        )

    return classifier


def remove_punctuation(args, xi):
    if args.text == "title":
        text_no_punct = str(xi["title"]).translate(
            str.maketrans("", "", string.punctuation)
        )
    elif args.text == "abstract":
        text_no_punct = str(xi["abstract"]).translate(
            str.maketrans("", "", string.punctuation)
        )
    else:
        text_no_punct = str(xi["title"]).translate(
            str.maketrans("", "", string.punctuation)
        ) + str(xi["abstract"]).translate(str.maketrans("", "", string.punctuation))
    return text_no_punct


def get_text(args, xi, stemming):
    if args.dataset_type == "original":
        text = stemming
    elif args.dataset_type == "enriched":
        if args.text == "title":
            text = xi["wikidata_title_entities"]
        elif args.text == "abstract":
            text = xi["wikidata_abstract_entities"]
        else:
            text = xi["wikidata_title_entities"] + xi["wikidata_abstract_entities"]
    else:
        if args.text == "title":
            xi["wikidata_title_entities"] = ast.literal_eval(
                xi["wikidata_title_entities"]
            )
            entities = " ".join([sub for sub in xi["wikidata_title_entities"]])
            text = stemming + entities
        elif args.text == "abstract":
            text = stemming + xi["wikidata_abstract_entities"]
        else:
            text = (
                stemming
                + xi["wikidata_title_entities"]
                + " "
                + xi["wikidata_abstract_entities"]
            )
    return text


def get_detector(args, pipeline_original):
    if args.classification_type == "adaptive":
        detector = pipeline_original["classifier"].drift_detector
    else:
        detector = drift.binary.DDM()
    return detector


def add_drifts_to_plot(drifts, plt):
    for d in drifts:
        plt.axvline(x=d["index"], color="r")


def classify(args, files, model_pkl_file):
    logging.info("Starting original experiment with: %s", str(args))

    ps = PorterStemmer()
    preds = []
    soma = 0
    preq = []
    drifts = []

    alpha = 0.99
    soma_a = 0
    nr_a = 0
    preq_a = []

    wind = 500
    soma_w = 0
    preq_w = []

    metric = metrics.Accuracy()
    accuracies = []
    index = 0

    feature_extraction = feature_extraction_model(args)
    classifier = classifier_model(args)

    pipeline_original = compose.Pipeline(
        ("feature_extraction", feature_extraction), ("classifier", classifier)
    )

    if os.path.exists(model_pkl_file):
        # Open the pickle file in binary read mode
        with open(model_pkl_file, "rb") as file:
            data = pickle.load(file)
            pipeline_original = data["model"]
            preq = data["preq"]
            preq_a = data["preq_a"]
            preq_w = data["preq_w"]
            accuracies = data["accuracies"]
            index = data["index"]
            preds = data["preds"]
            soma = data["soma"]
            drifts = data["drifts"]
            soma_a = data["soma_a"]
            nr_a = data["nr_a"]
            soma_w = data["soma_w"]
            metric = data["metric"]

    start_time_all = time.time()
    for file in files:
        start_time = time.time()
        dataset = manage_datasets.load_dataset(file)
        dataset["title_stemmed"] = pd.Series(dtype="string")
        dataset["text"] = pd.Series(dtype="string")

        target = dataset["category"]
        docs = dataset.drop(["category"], axis=1)

        i = 0

        # Perform the online classification loop
        for xi, yi in stream.iter_pandas(docs, target):
            i += 1
            # Preprocess the current instance
            text_no_punct = remove_punctuation(args, xi)
            word_tokens = word_tokenize(text_no_punct)
            stemming = " ".join([ps.stem(word) for word in word_tokens])

            # logging.info("Stemming = %s", stemming)
            xi["title_stemmed"] = stemming

            xi["text"] = get_text(args, xi, stemming)

            # logging.info(xi["text"])
            pipeline_original["feature_extraction"].learn_one(xi)
            transformed_doc = pipeline_original["feature_extraction"].transform_one(xi)
            # logging.info("Feature extraction result = %s", transformed_doc)

            # Make predictions and update the evaluation metric using the classifier
            y_pred = pipeline_original["classifier"].predict_one(transformed_doc)
            metric.update(yi, y_pred)
            accuracies.append(metric.get().real)
            if i == 10000:
                logging.info("Index = %s", index)
                logging.info("Accuracy = %s", metric.get().real)
                i = 0

            val = 0 if y_pred == yi else 1

            preds.append(val)
            soma += val
            preq.append(soma / (index + 1))

            soma_a = val + alpha * soma_a
            nr_a = 1 + alpha * nr_a
            preq_a.append(soma_a / nr_a)

            soma_w += val
            if index >= wind:
                soma_w = soma_w - preds[index - wind]
                preq_w.append(soma_w / 500)
            else:
                preq_w.append(soma_w / (index + 1))

            detector = get_detector(args, pipeline_original)

            _ = detector.update(val)
            if detector.drift_detected:
                logging.info(
                    "Change detected at index %s, input value: %s, predict value %s",
                    index,
                    yi,
                    y_pred,
                )
                drifts.append({"index": index, "input": yi, "predict": y_pred})

            # Update the classifier with the preprocessed features and the true label
            pipeline_original["classifier"].learn_one(transformed_doc, yi)
            index += 1

        summary_file = os.path.join(
            os.getcwd(),
            os.getenv("DATASETS_FOLDER")
            + args.results_dir
            + "/summary/"
            + args.dataset,
        )
        plot_file = os.path.join(
            os.getcwd(),
            os.getenv("DATASETS_FOLDER") + args.results_dir + "/plot/" + args.dataset,
        )
        plot_aux_file = os.path.join(
            os.getcwd(),
            os.getenv("DATASETS_FOLDER")
            + args.results_dir
            + "/plot_aux/"
            + args.dataset,
        )
        # tree_file = os.path.join(
        #     os.getcwd(),
        #     os.getenv("DATASETS_FOLDER")
        #     + args.results_dir
        #     + "/tree/"
        #     + os.path.splitext(os.path.basename(file))[0],
        # )

        # create plot
        _, ax = plt.subplots(figsize=(40, 20))
        ax.plot(range(index), preq, label="Prequential")
        ax.plot(range(index), preq_a, label="Prequential Alpha")
        ax.plot(range(index), preq_w, label="Prequential Window")
        add_drifts_to_plot(drifts, plt)
        ax.legend()
        plt.savefig(
            f"{plot_file}_{str(args.capitalization)}_{args.classification_type}"
            + f"_{args.feature_extraction}_{args.text}_{args.dataset_type}_plot.png"
        )
        plt.close()

        # create summary
        with open(
            f"{summary_file}_{str(args.capitalization)}_{args.classification_type}"
            + f"_{args.feature_extraction}_{args.text}_{args.dataset_type}_summary.csv",
            "w",
            newline="",
        ) as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(
                [
                    "nº documents",
                    "categories",
                    "mean_accuracy",
                    "time",
                    "time_all",
                    "drifts",
                    # "summary",
                ]
            )
            writer.writerow(
                [
                    index,
                    dataset["category"].nunique(),
                    metric.get().real,
                    (time.time() - start_time),
                    (time.time() - start_time_all),
                    len(drifts),
                    # pipeline_original["classifier"].summary,
                ]
            )
            f.close()

        # create plot aux
        df = pd.DataFrame({"preq": preq, "preq_a": preq_a, "preq_w": preq_w})
        df.to_csv(
            f"{plot_aux_file}_{str(args.capitalization)}_{args.classification_type}_"
            + f"{args.feature_extraction}_{args.text}_{args.dataset_type}_plot_aux.csv",
            index=False,
        )

        # with open(
        # plot_aux_file
        # + "_"
        # + str(args.capitalization)
        # + "_"
        # + args.classification_type
        # + "_"
        # + args.feature_extraction
        # + "_"
        # + args.text
        # + "_plot_aux.csv",
        # "w",
        # newline=""
        # ) as f:

        #     writer = csv.writer(f, delimiter=";")
        #     writer.writerow(["preq", "preq_a", "preq_w"])
        #     writer.writerow([preq, preq_a, preq_w])
        #     f.close()

        with open(
            f"{plot_aux_file}_{str(args.capitalization)}_{args.classification_type}_"
            + f"{args.feature_extraction}_{args.text}_{args.dataset_type}"
            + "_accuracy_aux.csv",
            "w",
            newline="",
        ) as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(["accuracy"])
            writer.writerow([accuracies])
            f.close()

        # create tree
        # with open(
        #     f"{tree_file}_{str(args.capitalization)}_{args.classification_type}_"
        #     + f"{args.feature_extraction}_{args.text}_tree.dot",
        #     "w",
        # ) as f:
        #     f.write(str(pipeline_original["classifier"].draw()))

        with open(model_pkl_file, "wb") as model_file:
            model_to_file = {
                "model": pipeline_original,
                "preq": preq,
                "preq_a": preq_a,
                "preq_w": preq_w,
                "accuracies": accuracies,
                "index": index,
                "preds": preds,
                "soma": soma,
                "drifts": drifts,
                "soma_a": soma_a,
                "nr_a": nr_a,
                "soma_w": soma_w,
                "metric": metric,
            }
            pickle.dump(model_to_file, model_file)
        logging.info(model_to_file)
        send2trash(file)


def main():
    args = setup.get_arg_parser_classification().parse_args()
    start_time = setup.initialize(
        "new_experiment_" + str(args.capitalization) + "_" + args.dataset
    )
    in_directory = os.path.join(
        os.getcwd(), os.getenv("DATASETS_FOLDER") + args.input_dir
    )
    tmp_directory = os.path.join(
        os.getcwd(), os.getenv("DATASETS_FOLDER") + args.tmp_dir
    )
    if args.dataset_format == "file":
        if args.with_copy == "yes":
            files_copy = realsorted(
                glob.glob(in_directory + constants.FILE_EXTENSION_SEARCH)
            )
            # logging.info(files_copy)
            for file in files_copy:
                shutil.copy2(file, tmp_directory)
        files = realsorted(glob.glob(tmp_directory + constants.FILE_EXTENSION_SEARCH))
    else:
        if args.with_copy == "yes":
            logging.info(in_directory)
            files_copy = natsorted(
                glob.glob(in_directory + constants.FILE_EXTENSION_SEARCH)
            )
            logging.info(files_copy)
            for file in files_copy:
                shutil.copy2(file, tmp_directory)
        files = natsorted(glob.glob(tmp_directory + constants.FILE_EXTENSION_SEARCH))

    models_folder = os.getenv("MODELS_FOLDER")
    model_pkl_file = os.path.join(
        os.getcwd(),
        f"{models_folder}model_dt_{str(args.dataset)}_{str(args.capitalization)}_"
        + f"{args.classification_type}_{args.feature_extraction}_{args.text}"
        + f"_{args.dataset_type}.pkl",
    )
    classify(args, files, model_pkl_file)

    logging.info("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    main()
