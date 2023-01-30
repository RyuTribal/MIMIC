package com.example.mimic;

public class MIMICError extends Exception {
    public MIMICError() {
    }

    public MIMICError(String message) {
        super(message);
    }

    @Override
    public String toString() {
        return "MIMICError{}";
    }
}
