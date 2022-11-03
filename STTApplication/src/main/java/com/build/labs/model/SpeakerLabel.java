package com.build.labs.model;

import com.fasterxml.jackson.annotation.JsonProperty;

public class SpeakerLabel {

	@JsonProperty("from")
	private double from;
	@JsonProperty("to")
	private double to;
	@JsonProperty("speaker")
	private int speaker;
	@JsonProperty("confidence")
	private double confidence;
	@JsonProperty("final")
	private boolean final_val;

	@JsonProperty("from")
	public double getFrom() {
		return from;
	}

	@JsonProperty("from")
	public void setFrom(double from) {
		this.from = from;
	}

	@JsonProperty("to")
	public double getTo() {
		return to;
	}

	@JsonProperty("to")
	public void setTo(double to) {
		this.to = to;
	}

	@JsonProperty("speaker")
	public int getSpeaker() {
		return speaker;
	}

	@JsonProperty("speaker")
	public void setSpeaker(int speaker) {
		this.speaker = speaker;
	}

	@JsonProperty("confidence")
	public double getConfidence() {
		return confidence;
	}

	@JsonProperty("confidence")
	public void setConfidence(double confidence) {
		this.confidence = confidence;
	}

	@JsonProperty("final")
	public boolean isFinal_val() {
		return final_val;
	}

	@JsonProperty("final")
	public void setFinal_val(boolean final_val) {
		this.final_val = final_val;
	}

}
