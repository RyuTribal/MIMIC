package com.example.mimic;

public class MIMICSay extends Action {
    public MIMICSay(String animationName) {
        super(animationName);
    }

    @Override
    public void execute(boolean as_async) throws MIMICError {
        System.out.println("execute from MIMICSay");
    }
}
