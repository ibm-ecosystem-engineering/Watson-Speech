package com.build.labs.model;

import java.util.List;

public class AlternativeSpeaker {
	private String transcript;
	private Double confidence;
	private List timestamps;

	public String getTranscript() {
		return transcript;
	}

	public void setTranscript(String transcript) {
		this.transcript = transcript;
	}

	public Double getConfidence() {
		return confidence;
	}

	public void setConfidence(Double confidence) {
		this.confidence = confidence;
	}

	public List getTimestamps() {
		return timestamps;
	}

	public void setTimestamps(List timestamps) {
		this.timestamps = timestamps;
	}

}
