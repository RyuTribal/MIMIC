package com.example.mimic;

import android.os.Bundle;
import android.widget.ImageButton;

import com.aldebaran.qi.sdk.QiContext;
import com.aldebaran.qi.sdk.QiSDK;
import com.aldebaran.qi.sdk.RobotLifecycleCallbacks;
import com.aldebaran.qi.sdk.builder.ChatBuilder;
import com.aldebaran.qi.sdk.object.conversation.Chat;
import com.aldebaran.qi.sdk.object.conversation.Chatbot;
import com.aldebaran.qi.sdk.design.activity.RobotActivity;
import com.example.mimic.robot_processors.OpenAI_Bot;


public class MainActivity extends RobotActivity implements RobotLifecycleCallbacks{
    ImageButton speak_button;
    private static final String TAG = "Main";
    private boolean isSpeakButtonLongPressed = false;
    private Chat chat;
    private Chatbot bot;
    private QiContext context;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        // Register the RobotLifecycleCallbacks to this Activity.
        QiSDK.register(this, this);
    }

    @Override
    protected void onDestroy() {
        // Unregister the RobotLifecycleCallbacks for this Activity.
        QiSDK.unregister(this, this);
        super.onDestroy();
    }

    @Override
    public void onRobotFocusGained(QiContext qiContext) {
        // The robot focus is gained.
        /*Say say = SayBuilder.with(qiContext) // Create the builder with the context.
                .withText("Stop stealing code Oscar!") // Set the text to say.
                .build(); // Build the say action.

        // Execute the action.
        say.run();*/
        this.bot = new OpenAI_Bot(qiContext);
        this.context = qiContext;
        chat = ChatBuilder.with(context)
                .withChatbot(bot)
                .build();
        chat.async().run();
    }

    @Override
    public void onRobotFocusLost() {
        // The robot focus is lost.
        if (this.chat != null) {
            this.chat.removeAllOnStartedListeners();
        }
    }

    @Override
    public void onRobotFocusRefused(String reason) {
        // The robot focus is refused.
    }
}
