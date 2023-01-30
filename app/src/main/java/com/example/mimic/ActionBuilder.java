package com.example.mimic;

// For constructing some Action
public class ActionBuilder {
    private String actionAnimationName;
    private boolean actionIsAsync;

    public ActionBuilder is_async(boolean value) {
        this.actionIsAsync = value;
        return this;
    }

    public ActionBuilder animation_name(String value) {
        this.actionAnimationName = value;
        return this;
    }

    /*
    public Action build() {
        return new Action(actionAnimationName);
    }
    */
}
