package sppech.analysis;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.InputStream;
import java.util.Arrays;

import com.ibm.cloud.sdk.core.security.IamAuthenticator;
import com.ibm.watson.speech_to_text.v1.SpeechToText;
import com.ibm.watson.speech_to_text.v1.model.GetModelOptions;
import com.ibm.watson.speech_to_text.v1.model.RecognizeOptions;
import com.ibm.watson.speech_to_text.v1.model.SpeechModel;
import com.ibm.watson.speech_to_text.v1.model.SpeechRecognitionResults;

/***
 * 
 * This class uses for using the IBM STT service 
 * @author abhilashamangal
 *
 */

public class SpeechAnalysisApp 
{
	// intialise variable for all 
	public String apiKey = "y4gidGcq79dlijEC9plFhG1K9IGW19E7RrVlZIxrRRrk";
	public String serviceURL = "https://api.us-south.speech-to-text.watson.cloud.ibm.com/instances/4e5c7864-5621-4bb6-9611-c0ffeb331aac";
	public String modelFileName ="en-US_BroadbandModel";
	
	/***
	 * 
	 * @return
	 */
	public SpeechToText initalizeAuthentication()
	{
		IamAuthenticator authenticator = new IamAuthenticator(apiKey);
		SpeechToText speechToText = new SpeechToText(authenticator);
		speechToText.setServiceUrl(serviceURL);
		return speechToText;
	}
	/***
	 * 
	 * @param speechToText
	 * @return
	 */
	public SpeechModel getResultModel(SpeechToText speechToText)
	{
		// get Langauge pre defined model
		GetModelOptions getModelOptions = new GetModelOptions.Builder().modelId(modelFileName) .build();
		SpeechModel speechModel = speechToText.getModel(getModelOptions).execute().getResult();
		System.out.println(speechModel);
		return speechModel;
		
	}
	/***
	 * 
	 * @param fileName
	 * @param speechToText
	 */
	public void getSpeechToTextValue(String fileName, SpeechToText speechToText)
	{
		try {
			  RecognizeOptions recognizeOptions = new RecognizeOptions.Builder()
			    .audio(new FileInputStream(fileName))
			    .contentType("audio/mp3")
			    .model(modelFileName)
			    .wordAlternativesThreshold((float) 0.9)
			    .keywords(Arrays.asList("colorado", "tornado", "tornadoes"))
			    .keywordsThreshold((float) 0.5)
			    .build();
			  
			  SpeechRecognitionResults speechRecognitionResults =speechToText.recognize(recognizeOptions).execute().getResult();
			  
			  System.out.println(speechRecognitionResults);
			  } catch (FileNotFoundException e) {
			    e.printStackTrace();
			  }
	}
	
	public String getFilePath(String fileName)
	{
		ClassLoader classloader = Thread.currentThread().getContextClassLoader();
		File file = new File(classloader.getResource(fileName).getFile());
		return file.getAbsolutePath();
		
	}
	
	
	public static void main(String args[])
	{
		System.out.println("Speech Example -----");
		
		SpeechAnalysisApp speech = new SpeechAnalysisApp();
		
		String fileName = "sample-000000.mp3";
		String filePath = speech.getFilePath(fileName);
		
		SpeechToText speechToText = speech.initalizeAuthentication();
		speech.getSpeechToTextValue(filePath, speechToText);
			

		
	}

}
