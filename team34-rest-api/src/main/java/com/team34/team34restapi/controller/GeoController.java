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
@RequestMapping("/api/geo")
@CrossOrigin(origins = "*", allowedHeaders = "*")
public class GeoController {

    @Value("${couchip}")
    private String couchIp;

    @Value("${couchport}")
    private int couchPort;

    @RequestMapping(value = "/lga")
    @ResponseBody
    public String getAusLga() {
        ViewResult viewResult;
        CouchDbClient dbClient = getLgaClient();
        List<JsonObject> jsonObject;
        String json = "";
        int a = 0;
        try {
            List<String> allTweets = new Vector<String>();
            View view = dbClient.view("_all_docs");
            jsonObject = view.includeDocs(true).query(JsonObject.class);
            //List<JsonObject> endpoints = couchDbClient.view("_all_docs").includeDocs(true).query(JsonObject.class);
            json = new Gson().toJson(jsonObject);
        } catch (Exception ex) {
            ex.printStackTrace();
        } finally {
            dbClient.shutdown();
        }
        return json;
    }


    private CouchDbClient getLgaClient() {
        CouchDbClient dbClient = new CouchDbClient("aus_lga",
                true, "http", couchIp, couchPort, "admin", "admin");
        return dbClient;
    }

}