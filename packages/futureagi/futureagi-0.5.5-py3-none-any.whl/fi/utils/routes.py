from enum import Enum


class Routes(str, Enum):
    healthcheck = "healthcheck"

    # logging
    log_model = "sdk/api/v1/log/model/"

    # evaluation
    evaluate = "sdk/api/v1/eval/"
    evaluate_template = "sdk/api/v1/eval/{eval_id}/"

    # dataset
    dataset = "model-hub/develops"
    dataset_names = "model-hub/develops/get-datasets-names/"
    dataset_empty = "model-hub/develops/create-empty-dataset/"
    dataset_local = "model-hub/develops/create-dataset-from-local-file/"
    dataset_huggingface = "model-hub/develops/create-dataset-from-huggingface/"
    dataset_table = "model-hub/develops/{dataset_id}/get-dataset-table/"
    dataset_delete = "model-hub/develops/delete_dataset/"
    dataset_add_rows = "model-hub/develops/{dataset_id}/add_rows/"
    dataset_add_columns = "model-hub/develops/{dataset_id}/add_columns/"

    # prompt
    generate_prompt = "model-hub/prompt-templates/generate-prompt/"
    improve_prompt = "model-hub/prompt-templates/improve-prompt/"
    run_template = "model-hub/prompt-templates/{template_id}/run_template/"
    create_template = "model-hub/prompt-templates/create-draft/"
    delete_template = "model-hub/prompt-templates/{template_id}"
    get_template_by_id = "model-hub/prompt-templates/{template_id}"
    get_template_id_by_name = "model-hub/prompt-templates/"

    # model provider
    model_hub_api_keys = "model-hub/api-keys/"
    model_hub_default_provider = "model-hub/default-provider/"

    dataset_add_run_prompt_column = "model-hub/develops/add_run_prompt_column/"
    dataset_add_evaluation = "model-hub/develops/{dataset_id}/add_user_eval/"
    dataset_optimization_create = "model-hub/optimisation/create/"
