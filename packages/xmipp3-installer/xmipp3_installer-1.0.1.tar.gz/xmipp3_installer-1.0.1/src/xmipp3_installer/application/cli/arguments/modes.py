"""### Containis all mode constants needed for the argument parsing part of Xmipp's installation."""

from xmipp3_installer.application.cli import arguments
from xmipp3_installer.application.cli.arguments.params import (
  PARAM_SHORT, PARAM_JOBS, PARAM_BRANCH, PARAM_KEEP_OUTPUT, PARAM_OVERWRITE,
  PARAM_MODELS_DIRECTORY, PARAM_TEST_NAMES, PARAM_SHOW_TESTS, PARAM_GIT_COMMAND,
  PARAM_LOGIN, PARAM_MODEL_PATH, PARAM_UPDATE, PARAMS, SHORT_VERSION, LONG_VERSION
)

MODE = "mode"

# Mode list (alphabetical order)
MODE_ADD_MODEL = 'addModel'
MODE_ALL = 'all'
MODE_CLEAN_ALL = 'cleanAll'
MODE_CLEAN_BIN = 'cleanBin'
MODE_COMPILE_AND_INSTALL = 'compileAndInstall'
MODE_CONFIG_BUILD = 'configBuild'
MODE_CONFIG = 'config'
MODE_GET_MODELS = 'getModels'
MODE_GET_SOURCES = 'getSources'
MODE_GIT = 'git'
MODE_TEST = 'test'
MODE_VERSION = 'version'

# Modes with help message
MODES = {
	'General': {
		MODE_VERSION: ['Returns the version information. Add \'--short\' to print only the version number.'],
		MODE_COMPILE_AND_INSTALL: ['Compiles and installs Xmipp based on already obtained sources.'],
		MODE_ALL: [f'Default param. Runs {MODE_CONFIG}, {MODE_CONFIG_BUILD}, and {MODE_COMPILE_AND_INSTALL}.'],
		MODE_CONFIG_BUILD: ['Configures the project with CMake.']
	},
	'Config': {
		MODE_CONFIG: ['Generates a config file template with default values.'],
	},
	'Downloads': {
		MODE_GET_MODELS: [f'Download the DeepLearning Models at dir/models ({arguments.DEFAULT_MODELS_DIR} by default).'],
		MODE_GET_SOURCES: ['Clone all Xmipp\'s sources.']
	},
	'Clean': {
		MODE_CLEAN_BIN: ['Removes all compiled binaries.'],
		MODE_CLEAN_ALL: ['Removes all compiled binaries and sources, leaves the repository as if freshly cloned (without pulling).']
	},
	'Test': {
		MODE_TEST: ['Runs a given test.']
	},
	'Developers': {
		MODE_GIT: ['Runs the given git action for all source repositories.'],
		MODE_ADD_MODEL: [
			"Takes a DeepLearning model from the modelPath, makes a tgz of it and uploads the .tgz according to the <login>.",
			"This mode is used to upload a model folder to the Scipion/Xmipp server.",
			"Usually the model folder contains big files used to fed deep learning procedures"
			"with pretrained data. All the models stored in the server will be downloads"
			"using the 'get_models' mode or during the compilation/installation time"
			"or with scipion3 installb deepLearningToolkit modelsPath must be the absolute path.",
			"",
			"Usage: -> ./xmipp addModel <usr@server> <modelsPath> [--update]",
			"Steps:	0. modelName = basename(modelsPath) <- Please, check the folders name!",
			"        1. Packing in 'xmipp_model_modelName.tgz'",
			"        2. Check if that model already exists (use --update to override an existing model)",
			"        3. Upload the model to the server.",
			"        4. Update the MANIFEST file.",
			"",
			"The model name will be the folder name in <modelsPath>",
			"Must have write permisions to such machine."
		]
	}
}

# Arguments of each mode, sorted by group
MODE_ARGS = {
	MODE_VERSION: [PARAM_SHORT],
	MODE_COMPILE_AND_INSTALL: [PARAM_JOBS, PARAM_KEEP_OUTPUT],
	MODE_ALL: [PARAM_JOBS, PARAM_BRANCH, PARAM_KEEP_OUTPUT],
	MODE_CONFIG_BUILD: [PARAM_KEEP_OUTPUT],
	MODE_CONFIG: [PARAM_OVERWRITE],
	MODE_GET_MODELS: [PARAM_MODELS_DIRECTORY],
	MODE_GET_SOURCES: [PARAM_BRANCH, PARAM_KEEP_OUTPUT],
	MODE_CLEAN_BIN: [],
	MODE_CLEAN_ALL: [],
	MODE_TEST: [PARAM_TEST_NAMES, PARAM_SHOW_TESTS],
	MODE_GIT: [PARAM_GIT_COMMAND],
	MODE_ADD_MODEL: [PARAM_LOGIN, PARAM_MODEL_PATH, PARAM_UPDATE]
}

# Examples for the help message of each mode
MODE_EXAMPLES = {
	MODE_VERSION: [
		f'./xmipp {MODE_VERSION}',
		f'./xmipp {MODE_VERSION} {PARAMS[PARAM_SHORT][LONG_VERSION]}',
	],
	MODE_COMPILE_AND_INSTALL: [
		f'./xmipp {MODE_COMPILE_AND_INSTALL}',
		f'./xmipp {MODE_COMPILE_AND_INSTALL} {PARAMS[PARAM_JOBS][SHORT_VERSION]} 20',
	],
	MODE_ALL: [
		'./xmipp',
		f'./xmipp {MODE_ALL}',
		f'./xmipp {PARAMS[PARAM_JOBS][SHORT_VERSION]} 20',
		f'./xmipp {PARAMS[PARAM_BRANCH][SHORT_VERSION]} devel',
		f'./xmipp {MODE_ALL} {PARAMS[PARAM_JOBS][SHORT_VERSION]} 20 '
		f'{PARAMS[PARAM_BRANCH][SHORT_VERSION]} devel'
	],
	MODE_CONFIG_BUILD: [],
	MODE_CONFIG: [
		f'./xmipp {MODE_CONFIG} {PARAMS[PARAM_OVERWRITE][LONG_VERSION]}'
	],
	MODE_GET_MODELS: [
		f'./xmipp {MODE_GET_MODELS}',
		f'./xmipp {MODE_GET_MODELS} {PARAMS[PARAM_MODELS_DIRECTORY][SHORT_VERSION]} /path/to/my/model/directory'
	],
	MODE_GET_SOURCES: [
		f'./xmipp {MODE_GET_SOURCES}'
		f'./xmipp {MODE_GET_SOURCES} {PARAMS[PARAM_BRANCH][SHORT_VERSION]} devel'
	],
	MODE_CLEAN_BIN: [],
	MODE_CLEAN_ALL: [],
	MODE_TEST: [
		f'./xmipp {MODE_TEST} xmipp_sample_test',
		f'./xmipp {MODE_TEST} {PARAMS[PARAM_SHORT][LONG_VERSION]}',
	],
	MODE_GIT: [
		f'./xmipp {MODE_GIT} pull',
		f'./xmipp {MODE_GIT} checkout devel'
	],
	MODE_ADD_MODEL: [
		f'./xmipp {MODE_ADD_MODEL} myuser@127.0.0.1 /home/myuser/mymodel'
	]
}
