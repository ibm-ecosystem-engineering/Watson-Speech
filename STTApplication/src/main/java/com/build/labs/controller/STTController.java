package com.build.labs.controller;

import java.io.IOException;
import java.io.InputStream;
import java.net.URISyntaxException;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

import org.springframework.core.io.ClassPathResource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.multipart.MultipartFile;

import com.build.labs.model.Output;
import com.build.labs.model.OutputSpeaker;
import com.build.labs.model.Speaker;
import com.build.labs.model.SpeakerLabel;
import com.build.labs.model.Summary;
import com.build.labs.model.SummarySpeaker;
import com.build.labs.services.STTService;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.fasterxml.jackson.databind.ObjectMapper;

@Controller
public class STTController {

	private final STTService sttService;

	public STTController(STTService sttService) {
		super();
		this.sttService = sttService;
	}

	/*
	 * This method build the home page. This page can be accessible in different
	 * ways {"/", "", "/index", "/home"}, it returns the content in page index.html
	 * resides in src/main/resources/templates directory.
	 */
	@GetMapping({ "/", "", "/index", "/home" })
	public String homepage() {
		return "index";
	}

	/*
	 * This method handles the file upload and convert it to a transcript and return
	 * the transcript to index page with model attribute result and if result holds
	 * any value index page displays the result.
	 */
	@PostMapping(value = "/uploadFile", produces = { MediaType.APPLICATION_JSON_VALUE })
	public ResponseEntity<List<Output>> uploadFile(@RequestParam("file") MultipartFile multipartFile)
			throws IOException, URISyntaxException {

		try (InputStream inputStream = multipartFile.getInputStream()) {
			String transcript = sttService.transcriptAudio(inputStream);
			List<Output> outputList = formatOutput(transcript);
			return ResponseEntity.ok(outputList);

		} catch (IOException ioe) {
			throw new IOException("Could not upload file: ", ioe);
		}
	}

	@GetMapping("/transcript/{filename}")
	public String transcriptAudio(@PathVariable("filename") String filename, Model model)
			throws IOException, URISyntaxException {

		InputStream input = new ClassPathResource("static/audio/" + filename).getInputStream();
		InputStream input1 = new ClassPathResource("static/audio/" + filename).getInputStream();
		String transcript = "";
		String transcriptParam = "";
		if (filename.startsWith("samples")) {
			transcriptParam = sttService.transcriptAudioParameter(filename, input);
			transcript = sttService.transcriptAudioParameterData(input1);
			if (filename.contains("speaker")) {
				List<OutputSpeaker> outputListParam1 = formatOutputSpeaker(transcriptParam);
				model.addAttribute("resultParamSpeaker", outputListParam1);
			} else {
				List<Output> outputListParam = formatOutput(transcriptParam);
				model.addAttribute("resultParam", outputListParam);
			}

			List<Output> outputList = formatOutput(transcript);
			model.addAttribute("result", outputList);
			return "index";

		} else {
			transcript = sttService.transcriptAudio(input1);
			List<Output> outputList = formatOutput(transcript);
			outputList.forEach(o -> {
				System.out.println("confidence: " + o.getConfidence());
				System.out.println("transcript: " + o.getTranscript());
			});

			model.addAttribute("resultNP", outputList);
			return "index";

		}

	}

	@GetMapping("/transcript/{filename}/download")
	public ResponseEntity<String> download(@PathVariable("filename") String filename)
			throws IOException, URISyntaxException {
		String transcript = "";
		HttpHeaders header = new HttpHeaders();
		header.add(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=output.json");
		header.add("Cache-Control", "no-cache, no-store, must-revalidate");
		header.add("Pragma", "no-cache");
		header.add("Expires", "0");

		InputStream input = readFile(filename);
		if (filename.startsWith("samples"))
			transcript = sttService.transcriptAudioParameterData(input);
		else
			transcript = sttService.transcriptAudio(input);

		return ResponseEntity.ok().headers(header).contentLength(transcript.length())
				.contentType(MediaType.parseMediaType("application/json")).body(transcript);
	}

	@GetMapping("/transcript/all")
	public ResponseEntity<String> downloadAll() throws IOException, URISyntaxException {

		HttpHeaders header = new HttpHeaders();
		header.add(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=all.json");
		header.add("Cache-Control", "no-cache, no-store, must-revalidate");
		header.add("Pragma", "no-cache");
		header.add("Expires", "0");

		List<String> filenames = List.of("CallCenterSample3.wav", "CallCenterSample2.wav", "CallCenterSample1.wav");

		String transcript = "";
		String output = "";
		for (String filename : filenames) {
			if (filename.startsWith("samples"))
				output = sttService.transcriptAudioParameter(filename, readFile(filename));
			else
				output = sttService.transcriptAudio(readFile(filename));
			transcript = transcript + "File name: " + filename + "\n" + output + "\n";
		}

		return ResponseEntity.ok().headers(header).contentLength(transcript.length())
				.contentType(MediaType.parseMediaType("application/json")).body(transcript);
	}

	private InputStream readFile(String filename) throws IOException {
		return new ClassPathResource("static/audio/" + filename).getInputStream();
	}

	private List<Output> formatOutput(String outputResult) throws JsonMappingException, JsonProcessingException {
		ObjectMapper objectMapper = new ObjectMapper();
		Summary summary = objectMapper.readValue(outputResult, Summary.class);

		List<Output> outputList = summary.getResults().stream().map(result -> {
			List<Output> output = result.getAlternatives().stream().map(alternative -> {
				Output out = new Output();
				out.setConfidence(alternative.getConfidence());
				out.setTranscript(alternative.getTranscript());
				return out;
			}).collect(Collectors.toList());

			return output;
		}).flatMap(List::stream).collect(Collectors.toList());

		return outputList;

	}

	private List<OutputSpeaker> formatOutputSpeaker(String outputResult)
			throws JsonMappingException, JsonProcessingException {
		ObjectMapper objectMapper = new ObjectMapper();
		SummarySpeaker summary = objectMapper.readValue(outputResult, SummarySpeaker.class);
		List<SpeakerLabel> speaker_label = summary.getSpeakerLabels();
		int temp_speaker = 0;
		double from = 0.0;
		double to = 0.0;
		List<Speaker> speakerList = new ArrayList<>();
		for (int i = 0; i < speaker_label.size(); i++) {
			SpeakerLabel speaker = speaker_label.get(i);
			if (i == 0) {
				temp_speaker = speaker.getSpeaker();
				from = speaker.getFrom();
				to = speaker.getTo();
			} else if (temp_speaker == speaker.getSpeaker()) {
				to = speaker.getTo();
			} else if (temp_speaker != speaker.getSpeaker()) {
				Speaker speakerVal = new Speaker();
				speakerVal.setFrom(from);
				speakerVal.setTo(to);
				speakerVal.setSpeakerValue(temp_speaker);
				temp_speaker = speaker.getSpeaker();
				from = speaker.getFrom();
				to = speaker.getTo();
				speakerList.add(speakerVal);
			}

		}
		// To add last value
		Speaker speakerVal = new Speaker();
		speakerVal.setFrom(from);
		speakerVal.setTo(to);
		speakerVal.setSpeakerValue(temp_speaker);
		speakerList.add(speakerVal);

		List<OutputSpeaker> outputList = summary.getResults().stream().map(result -> {
			List<OutputSpeaker> output = result.getAlternatives().stream().map(alternative -> {
				OutputSpeaker out = new OutputSpeaker();
				out.setTranscript(alternative.getTranscript());
				List time_stamp = alternative.getTimestamps();
				double start_time = 0;
				double end_time = 0;
				for (int i = 0; i < time_stamp.size(); i++) {
					List time = (List) time_stamp.get(i);
					if (i == 0) {
						start_time = (double) time.get(1);
					} else {
						end_time = (double) time.get(2);
					}
				}
				for (int j = 0; j < speakerList.size(); j++) {
					Speaker speakerVal1 = speakerList.get(j);
					if (speakerVal1.getTo() >= end_time) {
						out.setConfidence("" + speakerVal1.getSpeakerValue());
						break;
					}

				}
				return out;
			}).collect(Collectors.toList());

			return output;
		}).flatMap(List::stream).collect(Collectors.toList());
		return outputList;

	}

	@GetMapping({ "/stream" })
	public String stream() {
		return "stream";
	}

	@GetMapping({ "/socket" })
	public String socket() {
		return "socket";
	}
}
