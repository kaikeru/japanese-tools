# Japanese Tools

Simple tools for learning Japanese hosted at http://nihongo.kaikeru.com.

### Prerequisites

Japanese Tools are built on [Node.js](https://nodejs.org) and [MongoDB](https://www.mongodb.com) for the backend storage so install both on your system if you wish to run the tools.

Not provided is the kanji data used by the tools. The stroke order can be compiled using the scripts in `/tools` and loaded in to the `/models/kanji.js` model.

### Installing
After cloning and installing Node and Mongo, you need to install the dependencies using `npm`.

```
npm install
```

Once all packages are installed you'll need to run [Gulp](http://gulpjs.com/) build for the frontend CSS and JavaScript.

```
gulp
```

or if you want to have the build on each frontend file change

```
gulp watch
```

### Running

#### npm
The system uses Node to run. The easiest way to run the tools is using `npm`.

```
npm start
```

#### node
Or you can use Node.

```
node bin/www
```

#### nodemon
I highly recommend installing [nodemon](https://github.com/remy/nodemon) for development purposes so that the system reloads changes if you make any coding changes.

```
nodemon
```

## Built With

* [Express](https://expressjs.com) - Express used for website backend.
* [Node](https://nodejs.org/en/) - Node JavaScript environment.
* [MongoDB](https://www.mongodb.com/) - The database layer.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* [KanjiVG](http://kanjivg.tagaini.net/) - Kanji stroke orders provided by KanjiVG under the [Creative Commons Attribution-Share Alike 3.0](http://creativecommons.org/licenses/by-sa/3.0/) license.
