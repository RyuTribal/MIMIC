package com.example.mimic;

// For constructing some Action
public class ActionBuilder {
    private String actionAnimationName;
    private boolean actionIsAsync;

    /**
     * @param value whether to use async
     * @return The ActionBuilder so that it can be reused
     */
    public ActionBuilder is_async(boolean value) {
        this.actionIsAsync = value;
        return this;
    }

    /**
     * @param value The name of the animation to use for the Action
     * @return The ActionBuilder so that it can be reused
     */
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
