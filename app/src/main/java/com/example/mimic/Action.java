package com.example.mimic;


import com.aldebaran.qi.sdk.object.actuation.Animation;

// All other types of actions should inherit from this abstract class, this means that
// a lot of different actions can be abstracted over through the same method (`Action.execute()`)
// probably. This makes it easy to use actions as new actions can be built using a /ver/ generic
// `ActionBuilder` object.
public class Action {
    public String getName() {
        return name;
    }

    private String name;
    private String animationName;

    public String getAnimationName() {
        return animationName;
    }


    public Action(String animationName) {
        this.animationName = animationName;
    }


    public void execute(boolean as_async) {

    }
}
