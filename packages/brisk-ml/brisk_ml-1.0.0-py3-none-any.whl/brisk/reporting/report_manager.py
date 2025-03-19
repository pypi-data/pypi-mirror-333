"""Generate HTML reports from evaluation results.

This module provides the ReportManager class for creating HTML reports from 
modelevaluation results. It generates structured reports with interactive 
navigation and visualization of model performance metrics.
"""

import ast
import collections
import datetime
import inspect
import json
import os
from PIL import Image
import shutil
from typing import Type, Union, Any

import jinja2
import joblib
import pandas as pd

from brisk.version import __version__

class ReportManager():
    """Create HTML reports from evaluation results.

    Parameters
    ----------
    result_dir : str
        Directory containing evaluation results
    experiment_paths : dict
        Mapping of experiment groups to their file paths
    output_structure : dict
        Structure definition for output report
    description_map : dict
        Mapping of objects to their descriptions

    Attributes
    ----------
    result_dir : str
        Directory containing evaluation results
    templates_dir : str
        Directory containing HTML templates
    styles_dir : str
        Directory containing CSS styles
    report_dir : str
        Directory for generated HTML report
    experiment_paths : dict
        Mapping of experiment groups to their file paths
    env : jinja2.Environment
        Jinja2 environment for rendering templates
    method_map : OrderedDict
        Maps EvaluationManager methods to their reporting functions
    continuous_data_map : OrderedDict
        Maps continuous data files to reporting functions
    categorical_data_map : OrderedDict
        Maps categorical data files to reporting functions
    current_dataset : str or None
        Name of dataset currently being processed
    summary_metrics : defaultdict
        Nested dictionary of summary metrics
    output_structure : dict
        Maps experiment groups to their datasets
    description_map : dict
        Mapping of experiment groups to their descriptions
    """
    def __init__(
        self,
        result_dir: str,
        experiment_paths: dict,
        output_structure: dict,
        description_map: dict
    ):
        package_dir = os.path.dirname(os.path.abspath(__file__))
        self.result_dir = result_dir
        self.templates_dir = os.path.join(package_dir, "templates")
        self.styles_dir = os.path.join(package_dir, "styles")

        self.report_dir = os.path.join(result_dir, "html_report")
        self.experiment_paths = experiment_paths
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.templates_dir),
            autoescape=jinja2.select_autoescape(["html", "xml"])
        )
        self.method_map = collections.OrderedDict([
            ("serialized_model", self.report_serialized_model),
            ("evaluate_model", self.report_evaluate_model),
            ("evaluate_model_cv", self.report_evaluate_model_cv),
            ("compare_models", self.report_compare_models),
            ("confusion_matrix", self.report_confusion_matrix),
            ("plot_pred_vs_obs", lambda data, metadata: self.report_image(
                data, metadata, title="Predicted vs Observed Plot"
                )),
            ("plot_learning_curve", lambda data, metadata: self.report_image(
                data, metadata, title="Learning Curve", max_width="80%"
                )),
            ("plot_feature_importance", lambda data, metadata:
                self.report_image(
                    data, metadata, title="Feature Importance"
                )
            ),
            ("plot_residuals", lambda data, metadata: self.report_image(
                data, metadata, title="Residuals (Observed - Predicted)"
            )),
            ("plot_model_comparison", lambda data, metadata: self.report_image(
                data, metadata, title="Model Comparison Plot"
            )),
            ("plot_confusion_heatmap", lambda data, metadata: self.report_image(
                data, metadata, title="Confusion Matrix Heatmap"
            )),
            ("plot_roc_curve", lambda data, metadata: self.report_image(
                data, metadata, title="ROC Curve"
            )),
            ("plot_precision_recall_curve", lambda data, metadata:
                self.report_image(
                    data, metadata, title="Precision Recall Curve"
                )
            ),
            ("hyperparameter_tuning", lambda data, metadata: self.report_image(
                data, metadata, title="Hyperparameter Tuning"
            ))
        ])

        self.continuous_data_map = collections.OrderedDict([
            ("correlation_matrix.png", self.report_correlation_matrix),
            ("continuous_stats.json", self.report_continuous_stats),
        ])

        self.categorical_data_map = collections.OrderedDict([
            ("categorical_stats.json", self.report_categorical_stats),
        ])

        self.current_dataset = None
        self.summary_metrics = collections.defaultdict(
            lambda: collections.defaultdict(dict)
        )
        self.output_structure = output_structure
        self.description_map = description_map

    def create_report(self) -> None:
        """Generate the complete HTML report.

        Creates index page and all experiment pages, copies required CSS files,
        and generates navigation structure.
        """
        os.makedirs(self.report_dir, exist_ok=True)

        # Step 1: Create navigation data structure
        groups = []
        navigation_map = {}

        for group_name, datasets in self.experiment_paths.items():
            group_data = {
                "name": group_name,
                "datasets": []
            }

            for dataset_name, experiments in datasets.items():
                dataset_data = {
                    "name": dataset_name,
                    "experiments": list(experiments.keys())
                }
                group_data["datasets"].append(dataset_data)

                # Create ordered list of experiments for navigation
                exp_list = []
                for exp_name, exp_dir in experiments.items():
                    filename = f"{dataset_name}_{exp_name}"
                    exp_list.append({
                        "name": exp_name,
                        "filename": filename,
                        "dir": exp_dir
                    })

                # Set up navigation links for each experiment
                for i, exp in enumerate(exp_list):
                    prev_exp = exp_list[i-1] if i > 0 else None
                    next_exp = exp_list[i+1] if i < len(exp_list)-1 else None

                    navigation_map[exp["filename"]] = {
                        "prev": prev_exp["filename"] if prev_exp else None,
                        "next": next_exp["filename"] if next_exp else None,
                        "group": group_name,
                        "dataset": dataset_name
                    }

                    # Create experiment page with navigation info
                    self.create_experiment_page(
                        exp["dir"],
                        f"{group_name}/{dataset_name}",
                        navigation_map[exp["filename"]]
                    )

                # Create dataset page
                self.create_dataset_page(group_name, dataset_name)

            groups.append(group_data)

        # Create summary table
        summary_table_html = None
        if self.summary_metrics:
            summary_table_html = self.generate_summary_tables()

        # Copy CSS files
        for css_file in ["index.css", "experiment.css", "dataset.css"]:
            shutil.copy(
                os.path.join(self.styles_dir, css_file),
                os.path.join(self.report_dir, css_file)
            )

        # Render the index page
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        index_template = self.env.get_template("index.html")
        index_output = index_template.render(
            groups=groups,
            timestamp=timestamp,
            summary_table=summary_table_html,
            version=__version__,
            description_map=self.description_map
        )

        index_path = os.path.join(self.report_dir, "index.html")
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(index_output)

    def create_experiment_page(
        self,
        experiment_dir: str,
        dataset: str,
        navigation: dict
    ) -> None:
        """Create HTML page for a single experiment.

        Parameters
        ----------
        experiment_dir : str
            Directory containing experiment results
        dataset : str
            Name of the dataset used
        navigation : dict
            Navigation links for previous/next experiments
        """
        self.current_dataset = dataset
        experiment_template = self.env.get_template("experiment.html")
        experiment_name = os.path.basename(experiment_dir)
        dataset_name = os.path.splitext(os.path.basename(dataset))[0]
        filename = f"{dataset_name}_{experiment_name}"
        files = os.listdir(experiment_dir)

        # Step 1: Process file metadata
        file_metadata = {}
        for file in files:
            file_path = os.path.join(experiment_dir, file)
            if file.endswith(".json"):
                file_metadata[file] = self._get_json_metadata(file_path)
            if file.endswith(".png"):
                file_metadata[file] = self._get_image_metadata(file_path)
            if file.endswith(".pkl"):
                file_metadata[file] = {"method": "serialized_model"}

        # Step 2: Prepare content based on extracted metadata
        content = []

        for creating_method, reporting_method in self.method_map.items():
            matching_files = [
                (file, metadata) for file, metadata in file_metadata.items()
                if metadata["method"] == creating_method
            ]

            for file, metadata in matching_files:
                file_path = os.path.join(experiment_dir, file)
                data = self._load_file(file_path)
                content.append(reporting_method(data, metadata))

        content_str = "".join(content)

        # Step 3: Render the experiments page
        experiment_output = experiment_template.render(
            experiment_name=experiment_name,
            file_metadata=file_metadata,
            content=content_str,
            version=__version__,
            navigation=navigation
        )
        experiment_page_path = os.path.join(self.report_dir, f"{filename}.html")
        with open(experiment_page_path, "w", encoding="utf-8") as f:
            f.write(experiment_output)

    def create_dataset_page(self, group_name: str, dataset_name: str) -> None:
        """Creates an HTML page showing data split distribution information.
        
        Parameters
        ----------
        group_name : str
            Name of the experiment group
        dataset_name : str
            Name of the dataset
        """
        dataset_template = self.env.get_template("dataset.html")
        dataset_dir = os.path.join(
            self.result_dir, group_name, dataset_name, "split_distribution"
        )

        files = os.listdir(dataset_dir)
        content = []

        continuous_present = any(
            file.startswith("continuous_") for file in files
        )
        if continuous_present:
            content.append("<h2>Continuous Features</h2>")
            for file, report_method in self.continuous_data_map.items():
                matching_files = [f for f in files if file in f]
                for match in matching_files:
                    file_path = os.path.join(dataset_dir, match)
                    content.append(report_method(file_path))

        categorical_present = any(
            file.startswith("categorical_") for file in files
        )
        if categorical_present:
            content.append("<h2>Categorical Features</h2>")
            for file, report_method in self.categorical_data_map.items():
                matching_files = [f for f in files if file in f]
                for match in matching_files:
                    file_path = os.path.join(dataset_dir, match)
                    content.append(report_method(file_path))

        content_str = "".join(content)
        rendered_html = dataset_template.render(
            group_name=group_name,
            dataset_name=dataset_name,
            content=content_str,
            version=__version__
        )

        # Include group name in output file path
        output_file_path = os.path.join(
            self.report_dir,
            f"{group_name}_{dataset_name}.html"
        )
        with open(output_file_path, "w", encoding="utf-8") as f:
            f.write(rendered_html)

    def _get_json_metadata(self, json_path: str) -> dict:
        """Extracts metadata from a JSON file.

        Parameters
        ----------
        json_path : str
            Path to the JSON file

        Returns
        -------
        dict
            The extracted metadata
        """
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                metadata = data.get("_metadata", {})
                if "models" in metadata and isinstance(metadata["models"], str):
                    metadata["models"] = ast.literal_eval(metadata["models"])
                return metadata
        except json.JSONDecodeError as e:
            print(f"JSON decode error in {json_path}: {e}")
            return {}

        except ValueError as e:
            print(f"Value error in {json_path}: {e}")
            return {}

    def _get_image_metadata(self, image_path: str) -> dict:
        """Extracts metadata from a PNG file.

        Parameters
        ----------
        image_path : str
            Path to the image file

        Returns
        -------
        dict
            The extracted metadata
        """
        try:
            with Image.open(image_path) as img:
                metadata = img.info
                if "models" in metadata and isinstance(metadata["models"], str):
                    metadata["models"] = ast.literal_eval(metadata["models"])
                return metadata
        except FileNotFoundError:
            print(f"File not found: {image_path}")
            return {}

        except OSError as e:
            print(f"OS error while opening {image_path}: {e}")
            return {}

        except ValueError as e:
            print(f"Value error while processing metadata in {image_path}: {e}")
            return {}

    def _load_file(self, file_path: str) -> Union[dict, str, Any]:
        """Loads the content of a file based on its extension.

        Parameters
        ----------
        file_path : str
            Path to the file to load

        Returns
        -------
        Union[dict, str, Any]
            The loaded content, depending on file type:
            
            * .json : dict
                Parsed JSON content
            * .png : str
                Path to the image file
            * .pkl : Any
                Unpickled Python object

        Raises
        ------
        ValueError
            If the file extension is not .json, .png, or .pkl
        IOError
            If there is an error reading the file
        """
        if file_path.endswith(".json"):
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        elif file_path.endswith(".png"):
            return file_path
        elif file_path.endswith(".pkl"):
            with open(file_path, "rb") as f:
                return joblib.load(f)
        else:
            raise ValueError(f"Unsupported file type: {file_path}")

    def report_evaluate_model(self, data: dict, metadata: dict) -> str:
        """Generates an HTML block for displaying evaluate_model results.

        Parameters
        ----------
        data : dict
            The evaluation data
        metadata : dict
            The metadata associated with the evaluation

        Returns
        -------
        str
            HTML block representing the evaluation results
        """
        # Extract relevant information
        metrics = {k: v for k, v in data.items() if k != "_metadata"}
        model_info = metadata.get("models", ["Unknown model"])
        model_names = ", ".join(model_info)

        # Create an HTML block for this result
        result_html = f"""
        <h2>Model Evaluation</h2>
        <p><strong>Model:</strong> {model_names}</p>
        <table>
            <thead>
                <tr><th>Metric</th><th>Score</th></tr>
            </thead>
            <tbody>
        """
        for metric, score in metrics.items():
            rounded_score = round(score, 5)
            result_html += f"<tr><td>{metric}</td><td>{rounded_score}</td></tr>"
        result_html += "</tbody></table>"

        return result_html

    def report_evaluate_model_cv(self, data: dict, metadata: dict) -> str:
        """Generates an HTML block for displaying cross-validated evaluation 
        results.

        Parameters
        ----------
        data : dict
            The evaluation data containing metric information
        metadata : dict
            The metadata associated with the evaluation

        Returns
        -------
        str
            HTML block representing the cross-validation results
        """
        def get_unique_key(summary_metrics, current_database, models):
            model_key = f"{models} (2)"
            counter = 2
            while model_key in summary_metrics[current_database]:
                counter += 1
                model_key = f"{models} ({counter})"
            return model_key


        model_info = metadata.get("models", ["Unknown model"])
        models = ", ".join(model_info)

        result_html_new = f"""
        <h2>Model Evaluation (Cross-Validation)</h2>
        <p><strong>Model:</strong> {models}</p>
        <table>
            <thead>
                <tr><th>Metric</th><th>All Scores</th><th>Mean Score</th><th>Std Dev</th></tr>
            </thead>
            <tbody>
        """

        if models in self.summary_metrics[self.current_dataset]:
            models = get_unique_key(
                self.summary_metrics, self.current_dataset, models
            )

        for metric, values in data.items():
            if metric != "_metadata":
                all_scores = ", ".join(
                    f"{score:.5f}" for score in values["all_scores"]
                )
                mean_score = round(values["mean_score"], 5)
                std_dev = round(values["std_dev"], 5)
                result_html_new += (
                    f"<tr><td>{metric}</td><td>{all_scores}</td>"
                    f"<td>{mean_score}</td><td>{std_dev}</td></tr>"
                )

                self.summary_metrics[self.current_dataset][models][metric] = {
                    "mean": mean_score,
                    "std_dev": std_dev
                }

        result_html_new += "</tbody></table>"
        return result_html_new

    def report_compare_models(self, data: dict, metadata: dict) -> str:
        """Generates an HTML block for displaying model comparison results.

        Parameters
        ----------
        data : dict
            The comparison results
        metadata : dict
            The metadata containing model information

        Returns
        -------
        str
            HTML block representing the comparison results
        """
        model_names = metadata.get("models", [])

        if not model_names:
            raise ValueError("No model names found in metadata.")

        metrics = list(next(iter(data.values())).keys())
        metric_data = {
            model_name: {metric: data[model_name][metric] for metric in metrics}
            for model_name in model_names if "differences" not in model_name
            }

        df = pd.DataFrame(metric_data)

        if "differences" in data:
            diff_data = {
                metric: {
                    pair: data["differences"][metric].get(pair, None)
                    for pair in data["differences"][metric]
                    }
                for metric in data["differences"]
            }
            diff_df = pd.DataFrame(diff_data).T
            df = pd.concat([df, diff_df], axis=1)

        # Generate the HTML table
        model_name = ", ".join(metadata.get("models", ["Unknown model"]))
        html_table = df.to_html(classes="table table-bordered", border=0)
        result_html = f"""
        <h2>Model Comparison</h2>
        <p><strong>Model:</strong> {model_name}</p>
        """
        result_html += html_table

        return result_html

    def report_image(
        self,
        data: str,
        metadata: dict,
        title: str,
        max_width: str = "100%"
    ) -> str:
        """Generates an HTML block for displaying an image plot.

        Parameters
        ----------
        data : str
            The path to the image file
        metadata : dict
            The metadata associated with the plot
        title : str
            The title to display above the image
        max_width : str, optional
            The maximum width of the image. Defaults to "100%".

        Returns
        -------
        str
            HTML block containing the image and its metadata
        """
        model_name = ", ".join(metadata.get("models", ["Unknown model"]))
        rel_img_path = os.path.relpath(data, self.report_dir)

        result_html = f"""
        <h2>{title}</h2>
        <p><strong>Model:</strong> {model_name}</p>
        <img 
            src="{rel_img_path}"
            alt="{title}"
            style="max-width:{max_width};
                   height:auto;
                   display: block;
                   margin: 0 auto;"
        >
        """
        return result_html

    def report_confusion_matrix(self, data: dict, metadata: dict) -> str:
        """Generates an HTML block for displaying the confusion matrix results.

        Parameters
        ----------
        data : dict
            The confusion matrix data, including the matrix itself and labels
        metadata : dict
            The metadata associated with the matrix

        Returns
        -------
        str
            HTML block representing the confusion matrix results
        """
        confusion_matrix = data.get("confusion_matrix", [])
        labels = data.get("labels", [])
        model_info = metadata.get("models", ["Unknown model"])
        model_names = ", ".join(model_info)

        # Check for binary classification
        if len(labels) == 2:
            cell_annotations = {
                (0, 0): "True Positive",
                (0, 1): "False Positive",
                (1, 0): "False Negative",
                (1, 1): "True Negative",
            }
        else:
            cell_annotations = {}

        result_html = f"""
        <h2>Confusion Matrix</h2>
        <p><strong>Model:</strong> {model_names}</p>
        <table>
            <thead>
                <tr>
                    <th></th>
                    {"".join(f"<th>{label}</th>" for label in labels)}
                </tr>
            </thead>
            <tbody>
        """
        for i, (label, row) in enumerate(zip(labels, confusion_matrix)):
            result_html += f"<tr><td><strong>{label}</strong></td>"
            for j, count in enumerate(row):
                annotation = cell_annotations.get((i, j), "")
                result_html += f"<td>{count} {annotation}</td>"
            result_html += "</tr>"
        result_html += "</tbody></table>"

        return result_html

    def report_serialized_model(
        self,
        data: dict,
        metadata: dict # pylint: disable=W0613
    ) -> str:
        """Generate an HTML section describing a serialized model.

        Parameters
        ----------
        data : dict
            The loaded joblib object containing the model
        metadata : dict
            The metadata containing model information

        Returns
        -------
        str
            HTML formatted string describing the model
        """
        model_name = data.__class__.__name__
        params = data.get_params()

        default_params = self.get_default_params(data.__class__)

        non_default_params = {
            param: value for param, value in params.items()
            if value != default_params.get(param)
        }

        html = [
            f"<h2>Summary: {model_name}</h2>",
            "<div class='model-details'>"
        ]

        if non_default_params:
            html.extend([
                "<p>Non-Default Parameters:</p>",
                "<table class='params-table'>",
                "<tr><th>Parameter</th><th>Value</th></tr>"
            ])

            for param, value in sorted(non_default_params.items()):
                html.append(f"<tr><td>{param}</td><td>{value}</td></tr>")

            html.extend([
                "</table>"
            ])
        else:
            html.append("<p>All parameters are using default values</p>")

        html.append("</div>")

        return "\n".join(html)

    def generate_summary_tables(self) -> str:
        """Generates sortable HTML summary tables for each dataset, displaying 
        model metrics.

        Returns
        -------
        str
            HTML block containing sortable summary tables for all datasets
        """
        summary_html = ""
        for dataset, models in self.summary_metrics.items():
            summary_html += f"<h2>Summary for {dataset}</h2>"
            all_metrics = set()
            for model_metrics in models.values():
                all_metrics.update(model_metrics.keys())

            summary_html += """
            <table class="sortable">
                <thead>
                    <tr>
            """

            # Add headers with onclick handlers
            summary_html += (
                '<th onclick="sortTable(this.closest(\'table\'), 0)">Model</th>'
                )
            for idx, metric in enumerate(all_metrics, 1):
                summary_html += (
                    f'<th onclick="sortTable(this.closest(\'table\'), {idx})">'
                    f'{metric}</th>'
                    )

            summary_html += "</tr></thead><tbody>"

            # Add rows for each model
            for model, metrics in models.items():
                summary_html += f"<tr><td>{model}</td>"
                for metric in all_metrics:
                    if metric in metrics:
                        mean_score = round(metrics[metric]["mean"], 3)
                        std_dev = round(metrics[metric]["std_dev"], 3)
                        summary_html += f"<td>{mean_score} ({std_dev})</td>"
                    else:
                        summary_html += "<td>N/A</td>"
                summary_html += "</tr>"

            summary_html += "</tbody></table>"

        return summary_html

    # Report Dataset Distribution
    def report_continuous_stats(self, file_path: str) -> str:
        """Generate HTML for continuous feature statistics.

        Parameters
        ----------
        file_path : str
            Path to JSON file containing continuous statistics

        Returns
        -------
        str
            HTML content showing statistics and distribution plots
        """
        with open(file_path, "r", encoding="utf-8") as file:
            stats_data = json.load(file)

        content = ""

        base_dir = os.path.dirname(file_path)
        for feature_name, stats in stats_data.items():
            image_path = os.path.join(
                base_dir, "hist_box_plot", f"{feature_name}_hist_box.png"
                )
            rel_image_path = os.path.relpath(
                image_path, self.report_dir
                )

            if os.path.exists(image_path):
                image_html = f"""
                    <div class="image-container">
                        <img
                            src="{rel_image_path}"
                            alt="{feature_name} histogram and boxplot">
                    </div>
            """
            else:
                image_html = f"No image found at {rel_image_path}"

            # Create a table for each feature
            feature_html = f"""
            <div class="feature-section">
                <h3>{feature_name}</h3>
                <div class="flex-container">
                    <div class="flex-item">
                        <table class="feature-table">
                            <thead>
                                <tr>
                                    <th>Statistic</th>
                                    <th>Train</th>
                                    <th>Test</th>
                                </tr>
                            </thead>
                            <tbody>
            """

            # List of statistics for the table rows
            stats_keys = [
                "mean", "median", "std_dev", "variance", "min", "max", 
                "range", "25_percentile", "75_percentile", "skewness", 
                "kurtosis", "coefficient_of_variation"
                ]

            for stat in stats_keys:
                train_value = stats["train"].get(stat, "N/A")
                test_value = stats["test"].get(stat, "N/A")

                if isinstance(train_value, (int, float)):
                    train_value = round(train_value, 5)
                if isinstance(test_value, (int, float)):
                    test_value = round(test_value, 5)

                feature_html += f"""
                            <tr>
                                <td>{stat.replace("_", " ").capitalize()}</td>
                                <td>{train_value}</td>
                                <td>{test_value}</td>
                            </tr>
                """

            feature_html += """
                        </tbody>
                    </table>
                </div>
            """
            feature_html += image_html
            feature_html += """
                    </div>
                </div>
                <br/>
            """

            content += feature_html
        return content

    def report_correlation_matrix(self, file_path: str) -> str:
        """Generate HTML for feature correlation matrix.

        Parameters
        ----------
        file_path : str
            Path to correlation matrix image

        Returns
        -------
        str
            HTML content showing correlation heatmap
        """
        relative_img_path = os.path.relpath(file_path, self.report_dir)
        result_html = f"""
        <h3>Correlation Matrix</h3>
        <div class="correlation-matrix-container">
            <img src="{relative_img_path}" alt="Correlation Matrix">
        </div>
        """
        return result_html

    def report_categorical_stats(self, file_path: str) -> str:
        """Generate HTML for categorical feature statistics.

        Parameters
        ----------
        file_path : str
            Path to JSON file containing categorical statistics

        Returns
        -------
        str
            HTML content showing statistics and pie charts
        """
        with open(file_path, "r", encoding="utf-8") as file:
            stats_data = json.load(file)

        base_dir = os.path.dirname(file_path)

        content = ""

        for feature_name, stats in stats_data.items():
            image_path = os.path.join(
                base_dir, "pie_plot", f"{feature_name}_pie_plot.png"
                )
            rel_image_path = os.path.relpath(image_path, self.report_dir)
            feature_html = f"<h3>{feature_name}</h3>"
            feature_html += """
            <div class="flex-container">
                <div class="flex-item">
                    <table class="categorical-feature-table">
                        <thead>
                            <tr>
                                <th>Statistic</th>
                                <th>Train</th>
                                <th>Test</th>
                            </tr>
                        </thead>
                        <tbody>
            """

            stat_keys = [
                "frequency", "proportion", "num_unique", "entropy", "chi_square"
                ]
            chi_square_keys = ["chi2_stat", "p_value", "degrees_of_freedom"]

            for stat in stat_keys:
                train_value = stats["train"].get(stat, "N/A")
                test_value = stats["test"].get(stat, "N/A")

                if stat == "frequency" and isinstance(train_value, dict):
                    train_value = "<br>".join(
                        [f"{key}: {value}"
                         for key, value in sorted(train_value.items())]
                        )
                    test_value = "<br>".join(
                        [f"{key}: {value}"
                         for key, value in sorted(test_value.items())]
                        )
                    feature_html += f"""
                        <tr>
                            <td>{stat.capitalize()}</td>
                            <td>{train_value}</td>
                            <td>{test_value}</td>
                        </tr>
                    """
                elif stat == "proportion" and isinstance(train_value, dict):
                    train_value = "<br>".join(
                        [f"{key}: {value * 100:.2f}%"
                         for key, value in sorted(train_value.items())]
                        )
                    test_value = "<br>".join(
                        [f"{key}: {value * 100:.2f}%"
                         for key, value in sorted(test_value.items())]
                        )
                    feature_html += f"""
                        <tr>
                            <td>{stat.capitalize()}</td>
                            <td>{train_value}</td>
                            <td>{test_value}</td>
                        </tr>
                    """
                # Formatting chi_square dictionary to split across rows
                elif stat == "chi_square" and isinstance(train_value, dict):
                    for chi_key in chi_square_keys:
                        feature_html += f"""
                            <tr>
                                <td>
                                    {chi_key.replace("_", " ").capitalize()}
                                </td>
                                <td>
                                    {train_value.get(chi_key, "N/A")}
                                </td>
                                <td>
                                    {test_value.get(chi_key, "N/A")}
                                </td>
                            </tr>
                        """
                    continue

                else:
                    feature_html += f"""
                        <tr>
                            <td>{stat.replace("_", " ").capitalize()}</td>
                            <td>{train_value}</td>
                            <td>{test_value}</td>
                        </tr>
                    """

            feature_html += """
                        </tbody>
                    </table>
                </div>
            """

            if os.path.exists(image_path):
                feature_html += f"""
                    <div class="pie-plot-container">
                        <img
                            src="{rel_image_path}"
                            alt="{feature_name} pie chart">
                    </div>
                """
            else:
                feature_html += f"<p>No image found at {rel_image_path}</p>"

            feature_html += "</div><br/>"
            content += feature_html

        return content

    def get_default_params(self, model_class: Type) -> dict:
        """Extracts default parameters from the model class.

        Parameters
        ----------
        model_class : Type
            The class of the model


        Returns
        -------
        dict
            A dictionary of default parameters
        """
        init_signature = inspect.signature(model_class.__init__)
        default_params = {}

        for param in init_signature.parameters.values():
            if param.default is not inspect.Parameter.empty:
                default_params[param.name] = param.default

        return default_params
