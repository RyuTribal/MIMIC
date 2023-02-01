package com.example.mimic;

import android.os.Bundle;
import android.util.Log;
import android.view.MotionEvent;
import android.view.View;
import android.widget.ImageButton;

import com.aldebaran.qi.sdk.QiContext;
import com.aldebaran.qi.sdk.QiSDK;
import com.aldebaran.qi.sdk.RobotLifecycleCallbacks;
import com.aldebaran.qi.sdk.builder.ChatBuilder;
import com.aldebaran.qi.sdk.builder.QiChatbotBuilder;
import com.aldebaran.qi.sdk.builder.SayBuilder;
import com.aldebaran.qi.sdk.builder.TopicBuilder;
import com.aldebaran.qi.sdk.object.conversation.Chat;
import com.aldebaran.qi.sdk.object.conversation.Chatbot;
import com.aldebaran.qi.sdk.object.conversation.QiChatbot;
import com.aldebaran.qi.sdk.object.conversation.Say;
import com.aldebaran.qi.sdk.design.activity.RobotActivity;
import com.aldebaran.qi.sdk.object.conversation.Topic;
import com.example.mimic.RobotProcessors.OpenAI_Bot;


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
        setContentView(R.layout.layout);
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
        this.speak_button = findViewById(R.id.pepper_talk);
        this.speak_button.setOnLongClickListener(speakHoldListener);
        this.speak_button.setOnTouchListener(speakTouchListener);
        this.bot = new OpenAI_Bot(qiContext);
        this.context = qiContext;
        chat = ChatBuilder.with(context)
                .withChatbot(bot)
                .build();
        chat.async().run();
    }

    public void RunChat(){

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

    // Here lies our logic for when the button is held down
    private View.OnLongClickListener speakHoldListener = new View.OnLongClickListener() {

        @Override
        public boolean onLongClick(View pView) {
            // Do something when your hold starts here.
            RunChat();
            isSpeakButtonLongPressed = true;
            return true;
        }
    };

    // Here lies our logic for when the button is released
    private View.OnTouchListener speakTouchListener = new View.OnTouchListener() {
        @Override
        public boolean onTouch(View view, MotionEvent motionEvent) {
            view.onTouchEvent(motionEvent);
            // We're only interested in when the button is released.
            if (motionEvent.getAction() == MotionEvent.ACTION_UP) {
                // We're only interested in anything if our speak button is currently pressed.
                if (isSpeakButtonLongPressed) {
                    // Do something when the button is released.
                    if (chat != null) {
                        chat.removeAllOnStartedListeners();
                    }
                    isSpeakButtonLongPressed = false;
                }
            }
            return false;
        }
    };
}
