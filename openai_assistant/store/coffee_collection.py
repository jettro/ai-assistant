import weaviate.classes.config as wvc

# Name,Price,Description,Ingredients,Ratio of Ingredients


def coffee_weaviate_properties():

    return [
        wvc.Property(name="name",
                     data_type=wvc.DataType.TEXT,
                     vectorize_property_name=False,
                     skip_vectorization=False),
        wvc.Property(name="description",
                     data_type=wvc.DataType.TEXT,
                     vectorize_property_name=False,
                     skip_vectorization=False),
        wvc.Property(name="price",
                     data_type=wvc.DataType.NUMBER,
                     vectorize_property_name=False,
                     skip_vectorization=True),
        wvc.Property(name="ingredients",
                     data_type=wvc.DataType.TEXT,
                     vectorize_property_name=False,
                     skip_vectorization=False),
        wvc.Property(name="ratio_ingredients",
                     data_type=wvc.DataType.TEXT,
                     vectorize_property_name=False,
                     skip_vectorization=True),
    ]
