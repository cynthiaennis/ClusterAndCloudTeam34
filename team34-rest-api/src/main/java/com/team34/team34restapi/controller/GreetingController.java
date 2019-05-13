package com.team34.team34restapi.controller;

import com.google.gson.Gson;
import com.google.gson.JsonObject;
import com.team34.team34restapi.model.Greeting;
import org.lightcouch.CouchDbClient;
import org.lightcouch.View;
import org.lightcouch.ViewResult;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;
import java.util.Vector;
import java.util.concurrent.atomic.AtomicLong;

@RestController()
@RequestMapping("/api/twitter")
@CrossOrigin(origins = "*", allowedHeaders = "*")
public class GreetingController {

    private static final String template = "Hello, %s!";
    private final AtomicLong counter = new AtomicLong();


    @RequestMapping("/greeting")
    public Greeting greeting(@RequestParam(value = "name", defaultValue = "World") String name) {
        return new Greeting(counter.incrementAndGet(),
                String.format(template, name));
    }

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
            int count = dbClient.view("application/location_count_all?group=true").queryForInt();

            json = new Gson().toJson(jsonObject);

        } catch (Exception ex) {
            ex.printStackTrace();
        } finally {
            dbClient.shutdown();
        }

        return json;
    }


    @RequestMapping(value = "/getauslga")
    @ResponseBody
    public String getAusLga() {
        ViewResult viewResult;
        CouchDbClient dbClient = getTwitterClient();
        List<JsonObject> jsonObject;
        String json = "";
        int a = 0;
        try {
            List<String> allTweets = new Vector<String>();
            View view = dbClient.view("geolocation_lga/geolocation_lga");
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
        CouchDbClient dbClient = new CouchDbClient("aus_lga",
                true, "http", "172.26.38.116", 5984, "admin", "admin");
        return dbClient;
    }
//    @RequestMapping("/getpositive")
//    public String getPossitive() {
//        ViewResult viewResult;
//        CouchDbClient dbClient2 = new CouchDbClient("new_twitter_search",
//                true, "http", "172.26.38.116", 5984, "admin", "admin");
//        List<JsonObject> jsonObject;
//        String json ="";
//        int a =0;
//        try {
//            List<String> allTweets = new Vector<String>();
//            View view = dbClient2.view("application/location_count_positive?group=true");
//            jsonObject = view.query(JsonObject.class);
//            //List<JsonObject> endpoints = couchDbClient.view("_all_docs").includeDocs(true).query(JsonObject.class);
//            json = new Gson().toJson(jsonObject);
//        } catch (Exception ex) {
//            ex.printStackTrace();
//        } finally {
//            dbClient2.shutdown();
//        }
//
//        return json;
//    }


    @RequestMapping(value = "/getnegative", method = RequestMethod.GET)
    public String getNegative() {
        ViewResult viewResult;
        CouchDbClient dbClient = getTwitterClient();   List<JsonObject> jsonObject;
        String json = "";
        int a = 0;
        try {
            List<String> allTweets = new Vector<String>();
            View view = dbClient.view("application/location_count_negative?group=true");
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
}