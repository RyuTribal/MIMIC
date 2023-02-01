package com.example.mimic.network;

import android.util.Log;

import com.google.gson.JsonObject;

import java.io.IOException;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class GPTConnector {
    APIInterface apiInterface;
    JsonObject request_params;
    public static final String TAG = "GPTConnector";
    public GPTConnector(String model, String prompt, double temperature, int max_tokens){
        this.apiInterface = GPTClient.getClient().create(APIInterface.class);
        this.request_params = new JsonObject();
        request_params.addProperty("model", model);
        request_params.addProperty("prompt", prompt);
        request_params.addProperty("temperature", temperature);
        request_params.addProperty("max_tokens", max_tokens);
    }

    public String GetResponse() throws IOException {
        Call<GPTResponse> gpt_call = apiInterface.getAnswer(this.request_params);
        GPTResponse resp = gpt_call.execute().body();
        return resp.choices.get(0).text;
    }

}
