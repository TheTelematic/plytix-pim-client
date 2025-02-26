import warnings


async def test_add_new_variant_to_product(
    plytix,
    product,
    new_product_data,
):
    new_product_data["sku"] = f"{new_product_data['sku']}-variant"

    result = await plytix.products.variants.add_variant_to_product(product.id, new_product_data["sku"])

    assert result.sku == new_product_data["sku"]

    try:
        # The only asserts about this field, to not spread the undocumented stuff
        assert "_parent_id" in result._undocumented_data
        assert result._undocumented_data["_parent_id"] == product.id
    except AssertionError:
        warnings.warn("The _parent_id is no longer available in the _undocumented_data, remove this assert.")


async def test_add_new_variant_to_product_with_label(
    plytix,
    product,
    new_product_data,
):
    new_product_data["sku"] = f"{new_product_data['sku']}-variant"
    new_product_data["label"] = "Variant"

    result = await plytix.products.variants.add_variant_to_product(
        product.id, new_product_data["sku"], new_product_data["label"]
    )

    assert result.sku == new_product_data["sku"]
    assert result.label == new_product_data["label"]


async def test_add_new_variant_to_product_with_attributes(
    plytix,
    product,
    product_attribute,
    new_product_data,
):
    new_product_data["sku"] = f"{new_product_data['sku']}-variant"
    new_product_data["attributes"] = {product_attribute.label: "blue"}

    result = await plytix.products.variants.add_variant_to_product(
        product.id, new_product_data["sku"], attributes=new_product_data["attributes"]
    )

    assert result.sku == new_product_data["sku"]
    assert result.attributes == new_product_data["attributes"]


async def test_add_new_variant_to_product_not_found(plytix):
    result = await plytix.products.variants.add_variant_to_product("not_found", "not_found")

    assert result is None


async def test_add_new_variants_to_products(
    plytix,
    product,
    new_product_data,
    product_attribute,
):
    new_product_data["sku"] = f"{new_product_data['sku']}-variant"

    result = await plytix.products.variants.add_variant_to_products(
        [
            (
                product.id,
                {"sku": new_product_data["sku"], "label": "Variant", "attributes": {product_attribute.label: "blue"}},
            )
        ]
    )

    assert result[0].sku == new_product_data["sku"]
    assert result[0].label == "Variant"
    assert result[0].attributes == {product_attribute.label: "blue"}


async def test_add_new_variants_to_products_not_found(plytix):
    result = await plytix.products.variants.add_variant_to_products(
        [("not_found", {"sku": "not_found", "label": "not_found", "attributes": {}})]
    )

    assert result == [None]
