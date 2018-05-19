package com.kaikeru.nihongo.api;

import io.vertx.config.ConfigRetriever;
import io.vertx.config.ConfigRetrieverOptions;
import io.vertx.config.ConfigStoreOptions;
import io.vertx.core.AbstractVerticle;
import io.vertx.core.Future;
import io.vertx.core.json.JsonObject;
import io.vertx.ext.mongo.MongoClient;
import io.vertx.ext.web.Router;
import io.vertx.ext.web.handler.LoggerFormat;
import io.vertx.ext.web.handler.LoggerHandler;
import io.vertx.ext.web.handler.ResponseContentTypeHandler;
import com.kaikeru.nihongo.api.controller.Controller;
import com.kaikeru.nihongo.api.controller.v1.ControllerV1;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Main class for the Snoozle Sports REST API. This starts all server contexts and wires all routing for the API.
 * Use the Controller to control the routing.
 *
 * @author Kyle Wagner
 * @see com.kaikeru.nihongo.api.controller.Controller
 */
public class Application extends AbstractVerticle{

    private final Logger logger = LoggerFactory.getLogger(Application.class);

    // TODO Mount as a property or ENV.
    final String PORT_STR = System.getenv().containsKey("PORT") ?
        System.getenv("PORT") : "8080";
    final int PORT = Integer.parseInt(PORT_STR);

    /**
     * Create a new server and add the top level routing.
     * @param future A future context we can use.
     * @throws Exception
     */
    @Override
    public void start(Future<Void> future) {

        ConfigStoreOptions mongoConfigStore = new ConfigStoreOptions()
            .setType("file")
            .setConfig(new JsonObject().put("path", "conf/mongo.json"));
        ConfigRetriever mongoConfigRet = ConfigRetriever.create(
            vertx,
            new ConfigRetrieverOptions().addStore(mongoConfigStore));

        mongoConfigRet.getConfig(ar -> {
            if (ar.failed()) {
                logger.error("Could not load MongoDB config.");
            } else {
                logger.info("Loaded MongoDB config.");
                JsonObject config = ar.result();
                MongoClient mongodbClient = MongoClient.createShared(vertx, config);

                // Main Router
                // Set the main router and the content
                Router mainRouter = Router.router(vertx);

                // Make everything have 'Content-Type: application/json' header.
                mainRouter.route("/*")
                    .handler(ResponseContentTypeHandler.create())
                    .handler(LoggerHandler.create(LoggerFormat.DEFAULT))
                    .produces("application/json");

                // Setup the Version routers
                Controller v1 = new ControllerV1(vertx, mongodbClient);
                mainRouter.mountSubRouter("/v1", v1.getRouter());

                // Create the server and mount the main router.
                vertx.createHttpServer()
                    .requestHandler(mainRouter::accept)
                    .listen(PORT, res -> {
                        if(res.succeeded()){
                            logger.info("Server up. Port: " + PORT);
                            future.complete();
                        }
                        else{
                            logger.error("Failed to launch server");
                            future.fail(res.cause());
                        }
                    });
            }
        });


    }
}
