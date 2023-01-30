package com.example.mimic;

import com.aldebaran.qi.sdk.QiContext;
import com.aldebaran.qi.sdk.builder.AnimateBuilder;
import com.aldebaran.qi.sdk.builder.AnimationBuilder;
import com.aldebaran.qi.sdk.object.actuation.Animate;
import com.aldebaran.qi.sdk.object.actuation.Animation;

public class MIMICAnimate extends Action {
    public MIMICAnimate(String animationName) {
        super(animationName);
    }

    @Override
    public void execute(boolean as_async, QiContext ctx) throws MIMICError {
        // Get the animation from the actionprocessor somehow

        Animation animation = ActionProcessor.getInstance().getAnimation(this.getAnimationName());

        Animate a = AnimateBuilder.with(ctx).withAnimation(animation).build();
        
        if (as_async)
            a.async().run();
        else
            a.run();

    }
}
