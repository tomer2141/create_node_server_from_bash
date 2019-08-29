import subprocess
import os
import errno
from pathlib import Path
import json


def create_file(path_to_file, what_to_write, what_is_happening):
    print(what_is_happening)
    f = open(path_to_file, "w+")
    f.write(what_to_write)
    f.close()


def add_script():
    with open('package.json') as json_file:
        data = json.load(json_file)
        data["scripts"]["start"] = "nodemon index.js"

        create_file("package.json", json.dumps(
            data, indent=4, sort_keys=True), "Creating script...")


def main():
    # Create the package.json file
    runInitBashCommand = "npm init"
    process = subprocess.run(
        runInitBashCommand, check=True, shell=True)

    # Install all the relevent packages
    addPackegesCommand = "npm add babel-polyfill babel-preset-es2015 babel-preset-stage-0 babel-register nodemon body-parser morgan cookie-parser"
    process = subprocess.run(
        addPackegesCommand, check=True, shell=True)

    # Create relevent files
    create_file(
        ".babelrc", '{\r\n"presets": ["es2015", "stage-0"]\r\n}', "Creating .babelrc file...")

    # Create the index file
    create_file("index.js", "require('babel-register');\r\nrequire('babel-polyfill');\r\nrequire('./server');",
                "Creating index file...")

    # Create the server folder
    try:
        os.makedirs("server", exist_ok=True)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    # Write to server folder
    create_file("server/index.js",
                "import express from 'express';\r\nimport middlewaresConfig from './config/middlewares';\r\nimport { AppRoutes } from './modules';\r\nimport http from 'http';\r\n\r\nconst app = express();\r\n\r\nconst server = http.Server(app);\r\n\r\n/**# Middle wares**/ \r\nmiddlewaresConfig(app);\r\napp.use('/', [AppRoutes]);\r\n\r\nconst PORT = process.env.PORT || 3000;\r\n\r\nserver.listen(PORT, err => {\r\nif (err) {\r\nconsole.error(err);\r\n} else {\r\nconsole.log(`App listen to port: ${PORT}`);\r\n}\r\n});", "Creating server index file...")

    # Create the config folder
    try:
        os.makedirs("server/config", exist_ok=True)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    # Write to config folder
    create_file("server/config/middlewares.js",
                "import bodyParser from 'body-parser';\r\nimport morgan from 'morgan';\r\nimport cookieParser from 'cookie-parser';\r\n\r\nexport default app => {\r\n   app.use(cookieParser());\r\n   app.use(bodyParser.json());\r\n   app.use(bodyParser.urlencoded({ extended: false }));\r\n   app.use(morgan('dev'));\r\n};", "Creating middlewares file...")

    # Create the modules folder
    try:
        os.makedirs("server/modules", exist_ok=True)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    # Write to modules folder
    create_file("server/modules/index.js", "export * from './calls';",
                "Creating modules index file...")

    # Create the calls folder nested for modules
    try:
        os.makedirs("server/modules/calls", exist_ok=True)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    # Write several files for calls
    # Write index file
    create_file("server/modules/calls/index.js",
                "import AppRoutes from './routes.js';\r\n\r\nexport { AppRoutes };", "Creating calls index file...")

    # Write routes file
    create_file("server/modules/calls/routes.js",
                "import { Router } from 'express';\r\nimport * as appController from './controller.js';\r\n\r\nconst routes = new Router();\r\n\r\nroutes.get('/example', appController.example);\r\n\r\nexport default routes;", "Creating routes file...")

    # Write controller file
    create_file("server/modules/calls/controller.js",
                "export const example = (req, res) => {\r\n   res.status(200).send('This is an example return Created with createnode by Tomer Sagiv');\r\n}", "Creating controller file...")

    # Add script to package.json file
    add_script()
    # print done
    print("Done creating node server by Tomer Sagiv \n Add your desired script in the package.json file")


main()
