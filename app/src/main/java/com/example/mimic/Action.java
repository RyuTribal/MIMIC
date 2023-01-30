package com.example.mimic;


import com.aldebaran.qi.sdk.QiContext;

// All other types of actions should inherit from this abstract class, this means that
// a lot of different actions can be abstracted over through the same method (`Action.execute()`)
// probably. This makes it easy to use actions as new actions can be built using a /ver/ generic
// `ActionBuilder` object.
public abstract class Action {
    public String getName() {
        return name;
    }

    private String name;
    private String animationName; // Since some actions (like talking) does not have a animation associated with it, this has to be nullable. I miss Option<T>.

    public String getAnimationName() {
        return animationName;
    }

    public Action(String animationName) {
        this.animationName = animationName;
    }
    public abstract void execute(boolean as_async, QiContext ctx) throws MIMICError;

    /*
    public void execute(boolean as_async) throws MIMICError {
        // Maybe make this throw a custom error on *some* conditions

        // So i guess that matching on the name of the action is how we do it...
        switch (this.getName().toLowerCase()) {
            case "say":
                // Create Say action and stuff here
                break;

            case "animation":
                // Do some action from a .qianim file
                break;

            default:
                // No matching string found
                throw new MIMICError("Invalid action name: " + this.getName());

        }
    }
     */
}
