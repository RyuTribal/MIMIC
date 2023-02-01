package com.example.mimic.RobotProcessors;

import android.util.Log;

import androidx.annotation.NonNull;

import com.aldebaran.qi.Future;
import com.aldebaran.qi.sdk.QiContext;
import com.aldebaran.qi.sdk.builder.SayBuilder;
import com.aldebaran.qi.sdk.object.conversation.BaseChatbot;
import com.aldebaran.qi.sdk.object.conversation.BaseChatbotReaction;
import com.aldebaran.qi.sdk.object.conversation.Phrase;
import com.aldebaran.qi.sdk.object.conversation.ReplyPriority;
import com.aldebaran.qi.sdk.object.conversation.Say;
import com.aldebaran.qi.sdk.object.conversation.SpeechEngine;
import com.aldebaran.qi.sdk.object.conversation.StandardReplyReaction;
import com.aldebaran.qi.sdk.object.locale.Locale;
import java.util.concurrent.CancellationException;
import java.util.concurrent.ExecutionException;

public class OpenAI_Bot extends BaseChatbot {

    private static final String TAG = "GPT-3";
    private static final String GPT_KEY = "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";
    private static final String ORG_ID = "org-fb6c7Suc8WM6vFIaa250yUhG";

    public OpenAI_Bot(QiContext context) {
        super(context);
    }

    @Override
    public StandardReplyReaction replyTo(@NonNull Phrase phrase, Locale locale) {
        if (phrase.getText() != null) {
            return new StandardReplyReaction(
                    new OpenAI_Reaction(getQiContext(), "Hello you"),
                    ReplyPriority.NORMAL);
        } else {
            return new StandardReplyReaction(
                    new OpenAI_Reaction(getQiContext(), "Jag är inte säker på hur jag ska svara på detta"),
                    ReplyPriority.FALLBACK);
        }
    }

    @Override
    public void acknowledgeHeard(Phrase phrase, Locale locale) {
        Log.i(TAG, "Last phrase heard by the robot and whose chosen answer is not mine: " + phrase.getText());
    }

    @Override
    public void acknowledgeSaid(Phrase phrase, Locale locale) {
        Log.i(TAG, "Another chatbot answered: " + phrase.getText());
    }


    class OpenAI_Reaction extends BaseChatbotReaction {

        private String answer;
        private Future<Void> fSay;

        OpenAI_Reaction(final QiContext context, String answer) {
            super(context);
            this.answer = answer;
        }

        @Override
        public void runWith(SpeechEngine speechEngine) {

            Say say = SayBuilder.with(speechEngine)
                    .withText(answer)
                    .build();
            fSay = say.async().run();

            try {
                fSay.get(); // Do not leave the method before the actions are done
            } catch (ExecutionException e) {
                Log.e(TAG, "Error during Say", e);
            } catch (CancellationException e) {
                Log.i(TAG, "Interruption during Say");
            }
        }

        @Override
        public void stop() {
            if (fSay != null) {
                fSay.cancel(true);
            }
        }
    }
}
