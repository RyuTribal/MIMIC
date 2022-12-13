package com.example.mimic;

import android.view.animation.Animation;

import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.HashMap;

// Executes the queued actions synchronously or asynchronously depending on the user
// Since using animations needs the specific files it makes sense to convert the `Action` into a
// pepper friendly executable object
public class ActionProcessor {
    // The queued actions to use for the next run.
    private ArrayList<Action> queued_actions = new ArrayList<Action>();


    // The available, loaded animations.
    private HashMap<String, Animation> animations = new HashMap<String, Animation>();

    public ActionProcessor() {}

    // Adds a action to be executed later
    public void queueAction(Action action) {
        this.queued_actions.add(action);
    }

    /**
     * Adds a Animation object to be used with a specified animation name.
     * Makes the Animation available for use.
     *
     * @param animationName The name of the animation
     * @param animation The animation object itself
     */
    public void add_animation(String animationName, Animation animation) {
        animations.put(animationName, animation);
    }

    public Action deleteAction(int index) {
        return this.queued_actions.remove(index);
    }

    public Action deleteAction(String name) {
        for (Action action :
                this.queued_actions) {
            if (action.getName().equals(name)) {
                return action;
            }
        }

        return null;
    }

    public void executeQueue(boolean asAsync) {
        for (Action action :
                this.queued_actions) {
            action.execute(asAsync);
        }
    }
}
