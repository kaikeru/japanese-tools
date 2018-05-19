package com.kaikeru.nihongo.api.controller;

import io.vertx.config.ConfigRetriever;
import io.vertx.config.ConfigRetrieverOptions;
import io.vertx.config.ConfigStoreOptions;
import io.vertx.core.Vertx;
import io.vertx.core.json.Json;
import io.vertx.core.json.JsonObject;
import io.vertx.ext.mongo.MongoClient;
import io.vertx.ext.web.Router;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Base Controller class for the routing of the endpoints. This provides a starting point for all other controllers
 * to create the necessary subroutes that are needed to keep the code readable.
 *
 * @author Kyle Wagner
 */
public abstract class Controller {

    private final Logger logger = LoggerFactory.getLogger(Controller.class);

    /**
     * This main router is shared by all children and shouldn't be overridden. Instead, use a sub route to apply the
     * necessary level of routing.
     *
     * The following example shows how a top level controller should route all sub controllers for better cuts between
     * the code.
     *
     * <code>
     *     mainRouter.mountSubRouter("/mlb/players", new KanjiController(vertx).getRouter());
     * </code>
     */
    protected Router mainRouter;

    public Controller(final Vertx vertx) {
        mainRouter = Router.router(vertx);
    }

    /**
     * Return the router for the controller.
     * @return Router for use in the service.
     */
    public Router getRouter() {
        return mainRouter;
    }
}
