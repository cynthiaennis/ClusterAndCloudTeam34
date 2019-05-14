package com.team34.team34restapi.controller;

import com.google.gson.Gson;
import com.google.gson.JsonObject;
import org.lightcouch.CouchDbClient;
import org.lightcouch.View;
import org.lightcouch.ViewResult;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Vector;

@RestController()
@RequestMapping("/api/twitter")
@CrossOrigin(origins = "*", allowedHeaders = "*")
public class TwitterController {

    @Value("${couchip}")
    private String couchIp;

    @Value("${couchport}")
    private int couchPort;


    @RequestMapping("/getall")
    @ResponseBody
    public String getAll() {
        ViewResult viewResult;
        CouchDbClient dbClient = getTwitterClient();
        List<JsonObject> jsonObject;
        String json = "";
        int a = 0;
        try {
            List<String> allTweets = new Vector<String>();
            View view = dbClient.view("application/location_count_all?group=true");
            jsonObject = view.query(JsonObject.class);
            //List<JsonObject> endpoints = couchDbClient.view("_all_docs").includeDocs(true).query(JsonObject.class);

            json = new Gson().toJson(jsonObject);

        } catch (Exception ex) {
            ex.printStackTrace();
        } finally {
            dbClient.shutdown();
        }
        return json;
    }

    private CouchDbClient getTwitterClient() {
        CouchDbClient dbClient = new CouchDbClient("new_twitter_search",
                true, "http", couchIp, couchPort, "admin", "admin");
        return dbClient;
    }


    @RequestMapping(value = "/getnegative", method = RequestMethod.GET)
    public String getNegative() {
        ViewResult viewResult;
        CouchDbClient dbClient = getTwitterClient();   List<JsonObject> jsonObject;
        String json = "";
        int a = 0;
        try {
            List<String> allTweets = new Vector<String>();
            View view = dbClient.view("application/location_count_negative");
            jsonObject = view.group(true).query(JsonObject.class);
            //List<JsonObject> endpoints = couchDbClient.view("_all_docs").includeDocs(true).query(JsonObject.class);

            //negative count / total count = percentage
            json = new Gson().toJson(jsonObject);
        } catch (Exception ex) {
            ex.printStackTrace();
        } finally {
            dbClient.shutdown();
        }
        return json;
    }
}