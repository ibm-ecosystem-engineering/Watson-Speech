package com.build.labs.services;

import java.io.IOException;
import java.io.InputStream;
import java.net.URISyntaxException;
import java.util.HashMap;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import com.build.labs.feignclient.SSTServingClient;

@Service
public class STTService {

	private static final String SPEAKER_LABELS = "speaker_labels";

	private static final String END_OF_PHRASE_SILENCE_TIME = "end_of_phrase_silence_time";

	private static final String SMART_FORMATTING = "smart_formatting";

	private static final String BACKGROUND_AUDIO_SUPPRESSION = "background_audio_suppression";

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

	public String transcriptAudioParameter(String fileName, InputStream inputStream)
			throws URISyntaxException, IOException {
		HashMap<String, String> params = new HashMap<>();
		System.out.println(fileName);
		if (fileName.contains("back")) {
			params.put(BACKGROUND_AUDIO_SUPPRESSION, "0.5");
			params.put(SMART_FORMATTING, "true");
		} else if (fileName.contains("end"))
			params.put(END_OF_PHRASE_SILENCE_TIME, "0.3");
		else if (fileName.contains("speaker")) {
			params.put(SPEAKER_LABELS, "true");
			params.put(SMART_FORMATTING, "true");
		}
		String result = postFeignClient.transcriptParameter(params, inputStream.readAllBytes());
		return result;
	}

	public String transcriptAudioParameterData(InputStream inputStream) throws URISyntaxException, IOException {
		String result = postFeignClient.transcriptTelephony(inputStream.readAllBytes());
		return result;
	}

}
