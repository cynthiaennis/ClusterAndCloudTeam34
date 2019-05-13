package com.team34.team34restapi.model;

import java.io.Serializable;

public class Greeting implements Serializable {

    public Greeting(long l, String format) {
        this.count = l;
        this.format = format;
    }

    private long count;
    private String format;

    public long getCount() {
        return count;
    }

    public void setCount(long count) {
        this.count = count;
    }

    public String getFormat() {
        return format;
    }

    public void setFormat(String format) {
        this.format = format;
    }
}
