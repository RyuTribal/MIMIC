package com.example.mimic;

import com.aldebaran.qi.sdk.QiContext;
import com.aldebaran.qi.sdk.builder.SayBuilder;
import com.aldebaran.qi.sdk.object.conversation.Say;

public class MIMICSay extends Action {
    String to_say;

    public MIMICSay(String to_say) {
        // Saying something shouldnt require a animation name.
        super(null);

        this.to_say = to_say;
    }

    @Override
    public void execute(boolean as_async, QiContext ctx) throws MIMICError {
        System.out.println("execute from MIMICSay");

        Say say = SayBuilder.with(ctx)
                // Maybe convert the string being said here to a Phrase
                .withText(this.to_say)
                .build();

        if (as_async) {
            say.async().run();
        } else {
            say.run();
        }

    }
}
