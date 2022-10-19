package com.build.labs.feignclient;

import java.util.Map;

import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;

@FeignClient(name = "fclient", url = "${client.post.baseurl}") 
public interface SSTServingClient {
	
public final String STT_REST_MAPPING = "/speech-to-text/api/v1/recognize?model=en-US_Multimedia";
public final String STT_REST_MAPPING1 = "/speech-to-text/api/v1/recognize?model=en-US_Telephony";
	
	@PostMapping(STT_REST_MAPPING)
    String transcript(@RequestBody byte[] body);
	
	@PostMapping(STT_REST_MAPPING1)
    String transcriptTelephony(@RequestBody byte[] body);
	
	@PostMapping(STT_REST_MAPPING1)
    String transcriptParameter(@RequestParam Map<String,String> params,@RequestBody byte[] body);
}