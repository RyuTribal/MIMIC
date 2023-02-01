package com.example.mimic.network;

import com.google.gson.JsonObject;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.http.Body;
import retrofit2.http.Headers;
import retrofit2.http.POST;

public interface APIInterface {
    @Headers({"Authorization: Bearer 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", "Content-Type: application/json", "OpenAI-Organization: org-fb6c7Suc8WM6vFIaa250yUhG"})
    @POST("/v1/completions")
    Call<GPTResponse> getAnswer(@Body JsonObject gptParams);

}
