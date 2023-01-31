package com.example.mimic;


import com.aldebaran.qi.sdk.QiContext;
import com.aldebaran.qi.sdk.object.actuation.Animation;

import java.util.ArrayList;
import java.util.HashMap;

// Executes the queued actions synchronously or asynchronously depending on the user
// Since using animations needs the specific files it makes sense to convert the `Action` into a
// pepper friendly executable object
public class ActionProcessor {
    // Since we only need one action processor throughout the entire application (i think)
    // maybe make this static or use singleton.

    private static ActionProcessor instance = null;


    // The queued actions to use for the next run.
    private ArrayList<Action> queued_actions = new ArrayList<Action>();


    // The available, loaded animations.
    private HashMap<String, Animation> animations = new HashMap<String, Animation>();

    private QiContext ctx;

    public ActionProcessor(QiContext ctx) {
        this.ctx = ctx;
    }

    /**
     * Adds a action to be executed by the ActionProcessor later.
     *
     * @param action The Action to execute
     */
    public void queueAction(Action action) {
        this.queued_actions.add(action);
    }

    /**
     * Adds a Animation object to be used with a specified animation name.
     * Makes the Animation available for use.
     *
     * @param animationName The name of the animation
     * @param animation     The animation object itself
     */
    public void add_animation(String animationName, Animation animation) {
        animations.put(animationName, animation);
    }

    /**
     * Deletes the Action at the specified index from the execution queue.
     * @param index The index of the Action to delete.
     * @return The deleted Action or null if none is deleted.
     */
    public Action deleteAction(int index) {
        return this.queued_actions.remove(index);
    }

    /**
     * Deletes the Action with the specified name from the execution queue.
     *
     * @param name The name of the action to delete from the queue
     * @return The deleted Action or null if none is deleted.
     */
    public Action deleteAction(String name) {
        // TODO: What if there are two actions in the queue with the same name and we want the latter to be removed?
        for (Action action :
                this.queued_actions) {
            if (action.getName().equals(name)) {
                return action;
            }
        }

        return null;
    }

    /**
     * Searches the ActionProcessor's stored animations to convert a string to a Animation object.
     *
     * @param name The name of the animation to search for
     * @return Returns the animation object (or null)
     */
    public Animation getAnimation(String name) {
        return this.animations.get(name);
    }

    public static ActionProcessor getInstance() {
        // Should "panic" or throw a exception if there is no instance but
        // there basically is NEVER not a instance so...

        if (instance == null)
            System.out.println("Youre gonna have a bad time!");

        return instance;
    }

    /**
     * Executes the queued actions.
     *
     * @param asAsync Whether or not to execute the queue in a asynchronous manner.
     */
    public void executeQueue(boolean asAsync) {
        // This execution requires some object *like* the robot context to actually execute on, keep this internally in the action processor in that case.
        for (Action action :
                this.queued_actions) {

            try {
                action.execute(asAsync, this.ctx);
            } catch (MIMICError e) {
                System.out.println(e);
            }
        }
    }
}
