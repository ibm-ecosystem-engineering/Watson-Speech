package com.build.labs.model;

public class OutputSpeaker {
	
	private String transcript;
	private String confidence;

	public OutputSpeaker() {

	}

	public OutputSpeaker(String transcript, String confidence) {
		this.transcript = transcript;
		this.confidence = confidence;
	}

	public String getTranscript() {
		return transcript;
	}

	public void setTranscript(String transcript) {
		this.transcript = transcript;
	}

	public String getConfidence() {
		return confidence;
	}

	public void setConfidence(String confidence) {
		this.confidence = confidence;
	}

	@Override
	public String toString() {
		return "Output [transcript=" + transcript + ", confidence=" + confidence + "]";
	}

}
