import tkinter as tk
from run_config_settings import *
import ttk

import data_loader as dl
from FeatureExtraction import short_time_fourier_transform, wavelet_transform, mel_frequency_cepstral_coefficients, spectral_density_estimation, no_feature_extraction
from NeuralNetwork import feed_forward_neural_network, convolutional_neural_network, recurrent_neural_network, radial_basis_function_neural_network
import main_program


class GUI(tk.Tk):

    feature_extraction_techniques = ["No Feature Extraction",
                                     "Short-time Fourier Transform",
                                     "Wavelet Transform",
                                     "Mel-frequency Cepstral Coefficients",
                                     "Spectral Density Estimation"
                                     ]
    neural_network_types = ["Recurrent Neural Network",
                            "Convolutional Neural Network",
                            "Standard Feed-forward Neural Network",
                            "Radial Basis Function Network"
                             ]
    cell_types = ["Basic LSTM Cell",
                  "Basic RNN Cell",
                  "GRU Cell"
                  ]


    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # self.center_window()

        self.build_parameter_menu()

    def build_parameter_menu(self):
        tk.Label(self, text="Feature extraction technique").grid(row=0)
        self.FEbox_value = tk.StringVar()
        self.FEbox = self.combo(self, self.feature_extraction_techniques, self.FEbox_value)
        self.FEbox.grid(row=0, column=1)
        self.FEbox.bind("<<ComboboxSelected>>", self.newFEselection)
        self.build_fe_options_menu()
        self.update_fe_options_menu()

        tk.Label(self, text="Neural Network type").grid(row=0, column=3)
        self.NNbox_value = tk.StringVar()
        self.NNbox = self.combo(self, self.neural_network_types, self.NNbox_value)
        self.NNbox.grid(row=0, column=4)
        self.NNbox.bind("<<ComboboxSelected>>", self.newNNselection)
        self.build_nn_options_menu()
        self.update_nn_options_menu()

        self.center_window()
        # self.start_program()

    def start_program(self):
        data_loader = dl.DataLoader(TEST_PERCENTAGE, SAMPLING_RATE)
        FEtype = self.FEbox.get()
        if FEtype == self.feature_extraction_techniques[0]:
            feature_extractor = no_feature_extraction.NoFE()
        elif FEtype == self.feature_extraction_techniques[1]:
            feature_extractor = short_time_fourier_transform.STFT(fft_window_size=int(self.fft_window_size_entry.get()))
        elif FEtype == self.feature_extraction_techniques[2]:
            feature_extractor = wavelet_transform.WaveletTransform()
        elif FEtype == self.feature_extraction_techniques[3]:
            feature_extractor = mel_frequency_cepstral_coefficients.MFCC(n_mfcc=int(self.n_mfcc_entry.get()))
        elif FEtype == self.feature_extraction_techniques[4]:
            feature_extractor = spectral_density_estimation.SpectralDensityEstimation()


        NNtype = self.NNbox.get()
        if NNtype == self.neural_network_types[2]:
            neural_network = feed_forward_neural_network.FeedForwardNN(hidden_layers=list(map(int, self.hidden_layers_entry.get().split())),
                                                                       activation_functions_type=list(map(int, self.activation_functions_entry.get().split())),
                                                                       enable_bias=True if self.bias_box.get() == "True" else False,
                                                                       learning_rate=float(self.learning_rate_entry.get()),
                                                                       dropout_rate=float(self.dropout_rate_entry.get()),
                                                                       epocs=int(self.training_iterations_entry.get()))
        elif NNtype == self.neural_network_types[1]:
            neural_network = convolutional_neural_network.ConvolutionalNN()
        elif NNtype == self.neural_network_types[0]:
            neural_network = recurrent_neural_network.RecurrentNN(hidden_layers=list(map(int, self.hidden_layers_entry.get().split())),
                                                                  activation_functions_type=list(map(int, self.activation_functions_entry.get().split())),
                                                                  enable_bias=True if self.bias_box.get() == "True" else False,
                                                                     learning_rate=float(self.learning_rate_entry.get()),
                                                                  dropout_rate=float(self.dropout_rate_entry.get()),
                                                                  cell_type=self.cell_types.index(self.cell_type_box.get()),
                                                                  time_related_steps=int(self.time_related_steps_entry.get()),
                                                                  epochs=int(self.training_iterations_entry.get()))
        elif NNtype == self.neural_network_types[3]:
            neural_network = radial_basis_function_neural_network.RadialBasisFunctionNN()

        main_thread = main_program.MainProgram(feature_extractor, neural_network, data_loader=data_loader)

    def combo(self, frame, box_values, box_value):
        box = ttk.Combobox(frame, width=30, textvariable=box_value)
        box['values'] = box_values
        box.current(0)
        return box

    def newFEselection(self, event):
        value_of_combo = self.FEbox.get()
        self.update_fe_options_menu()
        print(value_of_combo)

    def newNNselection(self, event):
        value_of_combo = self.NNbox.get()
        self.update_nn_options_menu()
        print(value_of_combo)

    def build_fe_options_menu(self):
        self.fft_window_size_label = tk.Label(self, text="FFT window size")
        fft_window_size_value = tk.IntVar()
        fft_window_size_value.set(FFT_WINDOW_SIZE)
        self.fft_window_size_entry = tk.Entry(self, textvariable=fft_window_size_value, width=32)

        self.n_mfcc_label = tk.Label(self, text="Number of coefficients")
        n_mfcc_value = tk.IntVar()
        n_mfcc_value.set(N_MFCC)
        self.n_mfcc_entry = tk.Entry(self, textvariable=n_mfcc_value, width=32)

    def update_fe_options_menu(self):
        self.fft_window_size_label.grid_forget()
        self.fft_window_size_entry.grid_forget()
        self.n_mfcc_label.grid_forget()
        self.n_mfcc_entry.grid_forget()

        value_of_combo = self.FEbox.get()
        index = self.feature_extraction_techniques.index(value_of_combo)
        if index == 0:
            pass
        elif index == 1:
            self.fft_window_size_label.grid(row=1, column=0)
            self.fft_window_size_entry.grid(row=1, column=1)
        elif index == 3:
            self.n_mfcc_label.grid(row=1, column=0)
            self.n_mfcc_entry.grid(row=1, column=1)

    def build_nn_options_menu(self):
        self.hidden_layers_label = tk.Label(self, text="Hidden layers")
        hidden_layers_value = tk.StringVar()
        hidden_layers_value.set(HIDDEN_LAYERS)
        self.hidden_layers_entry = tk.Entry(self, textvariable=hidden_layers_value, width=32)

        self.activation_functions_label = tk.Label(self, text="Activation functions")
        activation_functions_value = tk.StringVar()
        activation_functions_value.set(ACTIVATION_FUNCTIONS)
        self.activation_functions_entry = tk.Entry(self, textvariable=activation_functions_value, width=32)

        self.bias_label = tk.Label(self, text="Bias")
        self.bias_value = tk.BooleanVar()
        self.bias_box = self.combo(self, [False, True], self.bias_value)

        self.learning_rate_label = tk.Label(self, text="Learning rate")
        learning_rate_value = tk.DoubleVar()
        learning_rate_value.set(LEARNING_RATE)
        self.learning_rate_entry = tk.Entry(self, textvariable=learning_rate_value, width=32)

        self.dropout_rate_label = tk.Label(self, text="Dropout rate")
        dropout_rate_value = tk.DoubleVar()
        dropout_rate_value.set(DROPOUT_RATE)
        self.dropout_rate_entry = tk.Entry(self, textvariable=dropout_rate_value, width=32)

        self.training_iterations_label = tk.Label(self, text="Training iterations")
        training_iterations_value = tk.IntVar()
        training_iterations_value.set(EPOCS)
        self.training_iterations_entry = tk.Entry(self, textvariable=training_iterations_value, width=32)

        self.cell_type_label = tk.Label(self, text="Cell type")
        self.cell_type_value = tk.StringVar()
        self.cell_type_box = self.combo(self, self.cell_types, self.cell_type_value)

        self.time_related_steps_label = tk.Label(self, text="Time-related steps")
        time_related_steps_value = tk.IntVar()
        time_related_steps_value.set(RELATED_STEPS)
        self.time_related_steps_entry = tk.Entry(self, textvariable=time_related_steps_value, width=32)

        self.start_button = tk.Button(self, text="Start", width=20, command=self.start_program)

    def update_nn_options_menu(self):
        value_of_combo = self.NNbox.get()
        index = self.neural_network_types.index(value_of_combo)
        if index == 0 or index == 2:
            self.hidden_layers_label.grid(row=1, column=3)
            self.hidden_layers_entry.grid(row=1, column=4)
            self.activation_functions_entry.grid(row=2, column=4)
            self.activation_functions_label.grid(row=2, column=3)
            self.bias_label.grid(row=3, column=3)
            self.bias_box.grid(row=3, column=4)
            self.learning_rate_label.grid(row=4, column=3)
            self.learning_rate_entry.grid(row=4, column=4)
            self.dropout_rate_label.grid(row=5, column=3)
            self.dropout_rate_entry.grid(row=5, column=4)
            self.training_iterations_label.grid(row=6, column=3)
            self.training_iterations_entry.grid(row=6, column=4)

        if index == 0:
            self.cell_type_label.grid(row=7, column=3)
            self.cell_type_box.grid(row=7, column=4)
            self.time_related_steps_label.grid(row=8, column=3)
            self.time_related_steps_entry.grid(row=8, column=4)
            self.start_button.grid(row=9, column=2)
        elif index == 1:
            pass
        elif index == 2:
            self.cell_type_label.grid_forget()
            self.cell_type_box.grid_forget()
            self.time_related_steps_label.grid_forget()
            self.time_related_steps_entry.grid_forget()

            self.start_button.grid(row=7, column=2)

    def center_window(self):
        ws = self.winfo_screenwidth()  # width of the screen
        hs = self.winfo_screenheight()  # height of the screen
        w = 1013
        h = 250
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))



if __name__ == "__main__":
    app = GUI()
    app.mainloop()
