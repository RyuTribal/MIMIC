package com.example.mimic;

// For constructing some Action
public class ActionBuilder {
    private String actionAnimationName;
    private boolean actionIsAsync;
    private String actionName;

    /**
     * @param value whether to use async
     * @return The ActionBuilder so that it can be reused
     */
    public ActionBuilder is_async(boolean value) {
        this.actionIsAsync = value;
        return this;
    }

    public ActionBuilder action_name(String value) {
        this.actionName = value;
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
        if (this.actionName.equals("say")) {
            return MIMICSay(this.ac)
        } else if (this.actionName.equals("animate")) {

        }
    }
     */
}
