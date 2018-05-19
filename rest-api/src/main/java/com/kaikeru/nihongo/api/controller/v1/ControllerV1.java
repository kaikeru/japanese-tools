package com.kaikeru.nihongo.api.controller.v1;

import io.vertx.core.Vertx;
import com.kaikeru.nihongo.api.controller.Controller;
import io.vertx.ext.mongo.MongoClient;

/**
 * The Controller for the version 1 of the API.
 *
 * @author Kyle Wagner
 */
public class ControllerV1 extends Controller {

    /**
     * Create a new Controller for the V1 of the API. Mounts all other Controllers for the V1 API.
     * @param vertx The vertx instance to use for the controller.
     */
    public ControllerV1(final Vertx vertx, final MongoClient mongoDBClient) {
        super(vertx);
        this.mainRouter.mountSubRouter("/kanji", new KanjiController(vertx, mongoDBClient).getRouter());
    }
}
