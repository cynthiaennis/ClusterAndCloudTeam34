package com.team34.team34restapi.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Component
public class AppConfig {

    @Value("${couchip}")
    private String couchIp;

    @Value("${couchport}")
    private int couchPort;


    public String getCouchIp() {
        return couchIp;
    }

    public void setCouchIp(String couchIp) {
        this.couchIp = couchIp;
    }

    public int getCouchPort() {
        return couchPort;
    }

    public void setCouchPort(int couchPort) {
        this.couchPort = couchPort;
    }
}
