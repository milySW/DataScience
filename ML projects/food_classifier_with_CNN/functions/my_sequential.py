from keras.models import Sequential


class my_sequential(Sequential):
    def set_model(self, model):
        """Sets Keras model and writes graph if specified."""
        self.model = model
        with context.eager_mode():
            self._close_writers()
            if self.write_graph:
                with self._get_writer(self._train_run_name).as_default():
                    with summary_ops_v2.always_record_summaries():
                        # if not model.run_eagerly:
                        summary_ops_v2.graph(K.get_graph(), step=0)
                        summary_writable = (
                            # self.model._is_graph_network or  # pylint: disable=protected-access
                            self.model.__class__.__name__
                            == "Sequential"
                        )  # pylint: disable=protected-access
                        if summary_writable:
                            summary_ops_v2.keras_model("keras", self.model, step=0)
            if self.embeddings_freq:
                self._configure_embeddings()
