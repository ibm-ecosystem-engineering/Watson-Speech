package com.build.labs.services;

import java.io.IOException;
import java.io.InputStream;
import java.net.URISyntaxException;
import java.util.HashMap;
import java.util.Map;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import com.build.labs.feignclient.SSTServingClient;
import com.build.labs.model.Summary;
import com.fasterxml.jackson.databind.ObjectMapper;

@Service
public class STTService {
	
    private final SSTServingClient postFeignClient;
    
    @Value("${client.post.baseurl}")
    private String baseUrl;
	
	public STTService(SSTServingClient postFeignClient) {
		super();
		this.postFeignClient = postFeignClient;
	}
	
	public String transcriptAudio(InputStream inputStream) throws URISyntaxException, IOException {
		String result = postFeignClient.transcript(inputStream.readAllBytes());
		return result;
	}
	
	public String transcriptAudioParameter(String fileName,InputStream inputStream) throws URISyntaxException, IOException {
		HashMap<Object, Object> params = new HashMap<>();
		System.out.println(fileName);
		if(fileName.contains("back"))
		{
			params.put("background_audio_suppression", "0.5");
			params.put("smart_formatting", "true");
		}
		else if(fileName.contains("end"))
			params.put("end_of_phrase_silence_time", "0.3");
		else if(fileName.contains("speaker"))
		{
			params.put("speaker_labels", "true");
			params.put("smart_formatting", "true");
		}	
		System.out.println(fileName+"----"+params);
		String result = postFeignClient.transcriptParameter(params,inputStream.readAllBytes());
		return result;
	}
	public String transcriptAudioParameterData(InputStream inputStream) throws URISyntaxException, IOException {
		String result = postFeignClient.transcriptTelephony(inputStream.readAllBytes());
		return result;
	}
	
	
}
