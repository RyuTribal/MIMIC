package com.example.mimic.network;

import com.google.gson.annotations.SerializedName;

import java.util.ArrayList;

public class GPTResponse {
    @SerializedName("id")
    public String id;
    @SerializedName("object")
    public String object;
    @SerializedName("created")
    public int created;
    @SerializedName("model")
    public String model;
    @SerializedName("choices")
    public ArrayList<Choice> choices;
    @SerializedName("usage")
    public Usage usage;

    //Constructor


    public GPTResponse(String id, String object, int created, String model, ArrayList<Choice> choices, Usage usage) {
        this.id = id;
        this.object = object;
        this.created = created;
        this.model = model;
        this.choices = choices;
        this.usage = usage;
    }

    public class Choice{
        @SerializedName("text")
        public String text;
        @SerializedName("index")
        public int index;
        @SerializedName("logprobs")
        public Object logprobs;
        @SerializedName("finish_reason")
        public String finish_reason;
        public Choice(String text, int index, Object logprobs, String finish_reason){
            this.text = text;
            this.index = index;
            this.logprobs = logprobs;
            this.finish_reason = finish_reason;
        }
    }

    public class Usage{
        @SerializedName("prompt_tokens")
        public int prompt_tokens;
        @SerializedName("completion_tokens")
        public int completion_tokens;
        @SerializedName("total_tokens")
        public int total_tokens;
        public Usage(int prompt_tokens, int completion_tokens, int total_tokens){
            this.prompt_tokens = prompt_tokens;
            this.completion_tokens = completion_tokens;
            this.total_tokens = total_tokens;
        }
    }
}
