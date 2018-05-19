package com.kaikeru.nihongo.api.controller.v1;

import io.vertx.core.Vertx;
import io.vertx.core.http.HttpMethod;
import io.vertx.core.http.HttpServerResponse;
import io.vertx.core.json.JsonObject;
import io.vertx.ext.mongo.MongoClient;
import io.vertx.ext.web.RoutingContext;
import com.kaikeru.nihongo.api.controller.Controller;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * The controller for the Major League Baseball players API.
 *
 * Endpoints: /mlb/players, /mlb/players/{id}
 *
 * @author Kyle Wagner
 */
public class KanjiController extends Controller {

    private final Logger logger = LoggerFactory.getLogger(KanjiController.class);

    private MongoClient mdb;

    public KanjiController(Vertx vertx, final MongoClient mongoClient) {
        super(vertx);

        this.mdb = mongoClient;
        // Create the routes and set the handlers.
        mainRouter.route(HttpMethod.GET, "/:character").handler(this::getCharacter);
    }

    /**
     * Get single character
     * @param ctx The routing context passed to the handler.
     */
    private void getCharacter(RoutingContext ctx) {
        HttpServerResponse response = ctx.response();

        String character = ctx.pathParam("character");

        if(character.length() > 1) {
            ctx.fail(404);
        }

        JsonObject query = new JsonObject()
            .put("character", character);
        mdb.find("kanjis", query, res -> {
            if (res.succeeded()) {
                for (JsonObject json : res.result()) {
                    json.remove("_id");
                    json.remove("__v");
                    response.end(json.encodePrettily());
                }
            } else {
                logger.warn(res.cause().getMessage());
                ctx.fail(404);
            }
        });
    }

    private class Character {
        private String character;

        public Character(final String ch){
            this.character = ch;
        }

        public String getCharacter() {
            return character;
        }

        public void setCharacter(String character) {
            this.character = character;
        }
    }
}
