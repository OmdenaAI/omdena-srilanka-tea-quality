package com.example.imageclassifier;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import android.app.Activity;
import android.content.Intent;
import android.content.res.AssetFileDescriptor;
import android.graphics.Bitmap;
import android.graphics.Color;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

import com.github.mikephil.charting.charts.BarChart;
import com.github.mikephil.charting.charts.HorizontalBarChart;
import com.github.mikephil.charting.components.XAxis;
import com.github.mikephil.charting.data.BarData;
import com.github.mikephil.charting.data.BarDataSet;
import com.github.mikephil.charting.data.BarEntry;
import com.github.mikephil.charting.formatter.IndexAxisValueFormatter;

import org.tensorflow.lite.DataType;
import org.tensorflow.lite.Interpreter;
import org.tensorflow.lite.support.common.FileUtil;
import org.tensorflow.lite.support.common.TensorOperator;
import org.tensorflow.lite.support.common.TensorProcessor;
import org.tensorflow.lite.support.common.ops.NormalizeOp;
import org.tensorflow.lite.support.image.ImageProcessor;
import org.tensorflow.lite.support.image.TensorImage;
import org.tensorflow.lite.support.image.ops.ResizeOp;
import org.tensorflow.lite.support.image.ops.ResizeWithCropOrPadOp;
import org.tensorflow.lite.support.label.TensorLabel;
import org.tensorflow.lite.support.tensorbuffer.TensorBuffer;

import java.io.FileInputStream;
import java.io.IOException;
import java.nio.MappedByteBuffer;
import java.nio.channels.FileChannel;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;

public class MainActivity extends AppCompatActivity {

    protected Interpreter tflite;
    private MappedByteBuffer tfliteModel;
    private TensorImage inputImageBuffer;
    private int imageSizeX;
    private int imageSizeY;
    private TensorBuffer outputProbabilityBuffer;
    private TensorProcessor probabilityProcessor;
    private static final float IMAGE_MEAN = 0.0f;
    private static final float IMAGE_STD = 1.0f;
    private static final float PROBABILITY_MEAN = 0.0f;
    private static final float PROBABILITY_STD = 255.0f;
    private Bitmap bitmap;
    private List<String> labels;
    private HorizontalBarChart mBarChart;
    ImageView imageView;
    Uri imageUri;
    Button btnClassify;
    TextView prediction;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        imageView = (ImageView) findViewById(R.id.imageView);
        btnClassify = (Button) findViewById(R.id.classify);
        prediction = (TextView) findViewById(R.id.predictionTxt);

        //import image from gallery action
        imageView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent();
                intent.setType("image/*");
                intent.setAction(Intent.ACTION_GET_CONTENT);
                startActivityForResult(Intent.createChooser(intent, "Select Picture"), 12);
            }
        });

        //define the interpreter with tflite model
        try {
            tflite = new Interpreter(loadmodelfile(MainActivity.this));
        } catch (IOException e) {
            e.printStackTrace();
        }

        //classify btn on click listener
        btnClassify.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                int imageTensorIndex = 0;
                int[] imageShape = tflite.getInputTensor(imageTensorIndex).shape(); //{1, height, weight, 3}
                imageSizeX = imageShape[1];
                imageSizeY = imageShape[2];
                DataType imageDataType = tflite.getInputTensor(imageTensorIndex).dataType();

                int probabilityTensorIndex = 0;
                int[] probabilityShape = tflite.getOutputTensor(probabilityTensorIndex).shape(); // {1, NUM_CLASS}
                DataType probabilityDataType = tflite.getInputTensor(probabilityTensorIndex).dataType();

                inputImageBuffer = new TensorImage(imageDataType);
                outputProbabilityBuffer = TensorBuffer.createFixedSize(probabilityShape, probabilityDataType);
                probabilityProcessor = new TensorProcessor.Builder().add(getPostProcessorNormalizeOP()).build();

                inputImageBuffer = loadImage(bitmap);

                tflite.run(inputImageBuffer.getBuffer(), outputProbabilityBuffer.getBuffer().rewind());
                showresults();
            }
        });
    }

    //load the image and do the image processing
    private TensorImage loadImage(final Bitmap bitmap) {
        //load bitmap into TensorImage
        inputImageBuffer.load(bitmap);

        //create processor for the tensorflow
        int cropSize = Math.min(bitmap.getWidth(), bitmap.getHeight());

        ImageProcessor imageProcessor =
                new ImageProcessor.Builder()
                        .add(new ResizeWithCropOrPadOp(cropSize, cropSize))
                        .add(new ResizeOp(imageSizeX, imageSizeY, ResizeOp.ResizeMethod.NEAREST_NEIGHBOR))
                        .add(getPreProcessorNormalizeOP())
                        .build();
        return imageProcessor.process(inputImageBuffer);
    }


    //load the tflite model
    private MappedByteBuffer loadmodelfile(Activity activity) throws IOException {
        AssetFileDescriptor fileDescriptor = activity.getAssets().openFd("model.tflite");
        FileInputStream inputStream = new FileInputStream(fileDescriptor.getFileDescriptor());
        FileChannel fileChannel = inputStream.getChannel();
        long startoffset = fileDescriptor.getStartOffset();
        long declareLength = fileDescriptor.getDeclaredLength();
        return fileChannel.map(FileChannel.MapMode.READ_ONLY, startoffset, declareLength);
    }

    // normalize the image
    private TensorOperator getPreProcessorNormalizeOP() {
        return new NormalizeOp(IMAGE_MEAN, IMAGE_STD);
    }

    private TensorOperator getPostProcessorNormalizeOP() {
        return new NormalizeOp(PROBABILITY_MEAN, PROBABILITY_STD);
    }


    //create barchart
    public static void barChart(BarChart barChart, ArrayList<BarEntry> arrayList, final ArrayList<String> xAxisValues) {
        barChart.setDrawBarShadow(false);
        barChart.setFitBars(false);
        barChart.setDrawValueAboveBar(true);
        barChart.setMaxVisibleValueCount(25);
        barChart.setPinchZoom(true);
        barChart.setDrawGridBackground(false);

        BarDataSet barDataSet = new BarDataSet(arrayList, "Class");
        barDataSet.setColors(new int[]{Color.parseColor("blue"), Color.parseColor("red"),
                Color.parseColor("green"), Color.parseColor("yellow"), Color.parseColor("magenta"),
                Color.parseColor("gray")});

        BarData barData = new BarData(barDataSet);
        barData.setBarWidth(0.9f);
        barData.setValueTextSize(0f);

        barChart.setBackgroundColor(Color.WHITE); // add your color
        barChart.setDrawGridBackground(false);
        barChart.animateY(2000);

        //to set components of X axis
        XAxis xAxis = barChart.getXAxis();
        xAxis.setTextSize(13f);
        xAxis.setTextColor(Color.BLACK);
        xAxis.setPosition(XAxis.XAxisPosition.TOP_INSIDE);
        xAxis.setValueFormatter(new IndexAxisValueFormatter(xAxisValues));
        xAxis.setDrawGridLines(false);

        barChart.setData(barData);
    }

    //show results
    private void showresults() {
        try {
            labels = FileUtil.loadLabels(MainActivity.this, "labels.txt");
        } catch (IOException e) {
            e.printStackTrace();
        }

        Map<String, Float> labelsProbability = new TensorLabel(labels, probabilityProcessor.process(outputProbabilityBuffer))
                .getMapWithFloatValue();
        float maxValueinMap = (Collections.max(labelsProbability.values()));

        String[] label;
        Float[] label_probability;
        for (Map.Entry<String, Float> entry : labelsProbability.entrySet()) {
            label = labelsProbability.keySet().toArray(new String[0]);
            label_probability = labelsProbability.values().toArray(new Float[0]);

            mBarChart = findViewById(R.id.chart);
            mBarChart.getXAxis().setDrawGridLines(false);
            mBarChart.getAxisLeft().setDrawGridLines(false);

            //preparing the array list of bar entries
            ArrayList<BarEntry> barEntries = new ArrayList<>();
            for (int i = 0; i < label_probability.length; i++) {
                barEntries.add(new BarEntry(i, label_probability[i]*100));
            }

            //add values in X-axis
            ArrayList<String> xAxisName = new ArrayList<>();
            for (int i = 0; i < label.length; i++) {
                xAxisName.add(label[i]);
            }
            barChart(mBarChart, barEntries, xAxisName);
            prediction.setText("Prediction");
        }
    }


    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data)  {
        super.onActivityResult(requestCode, resultCode, data);

        if (requestCode == 12 && resultCode == RESULT_OK && data != null) {
            imageUri = data.getData();

            try {
                bitmap = MediaStore.Images.Media.getBitmap(getContentResolver(), imageUri);
                imageView.setImageBitmap(bitmap);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
}