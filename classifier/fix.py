import tensorflow as tf

# Load the model
model = tf.keras.models.load_model("models/model_1.h5")

# Function to remove the 'groups' argument from the DepthwiseConv2D layer
def remove_groups_from_layer(layer):
    if isinstance(layer, tf.keras.layers.DepthwiseConv2D):
        layer_config = layer.get_config()
        if 'groups' in layer_config:
            del layer_config['groups']
        return tf.keras.layers.DepthwiseConv2D.from_config(layer_config)
    return layer

# Apply the function to all layers in the model
model = tf.keras.models.clone_model(model, clone_function=remove_groups_from_layer)

# Save the modified model
model.save("models/modified_model.h5")
