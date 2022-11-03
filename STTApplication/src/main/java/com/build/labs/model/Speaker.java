package com.build.labs.model;

public class Speaker {

	private int speakerValue;
	private String transcript;
	private double from;
	private double to;

	public double getFrom() {
		return from;
	}

	public void setFrom(double from) {
		this.from = from;
	}

	public double getTo() {
		return to;
	}

	public void setTo(double to) {
		this.to = to;
	}

	public int getSpeakerValue() {
		return speakerValue;
	}

	public void setSpeakerValue(int speakerValue) {
		this.speakerValue = speakerValue;
	}

	public String getTranscript() {
		return transcript;
	}

	public void setTranscript(String transcript) {
		this.transcript = transcript;
	}

}
