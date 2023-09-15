from django.http import HttpResponse, JsonResponse
import requests
import json

# Create your views here.
def home(request):
    response = {
        "Greetings":"Welcome to Homedepot APIs",
        "endpoints":{
            'search': '/homedepot/search?keyword=<keyword>&sort_by=<sort_by>&page=<page>',
            'specific_product': '/homedepot/product?item_id=<item_id>',
            'review': '/homedepot/product/reviews?item_id=<item_id>&sort_by=<sort_by>&page=<page>',
        }
    }
    return JsonResponse(response)

def search_by_keyword(request):
    response_json = dict()
    if request.method == "GET":
        url = "https://www.homedepot.com/federation-gateway/graphql?opname=searchModel"
        print(request.GET)
        keyword = request.GET['keyword']
        if 'page' in request.GET:
            page = request.GET['page']
            startIndex = (int(page) - 1) * 24
        else:startIndex = 0

        sort_by_dict = {
            "field": str,
            "order": str
        }
        try:sort_by = request.GET['sort_by']
        except:sort_by = ''
        if 'sort_by' not in request.GET or sort_by == '':
            sort_by_dict['field'] = 'BEST_MATCH'
            sort_by_dict['order'] = 'ASC'
        else:

            if 'top_seller' in sort_by:
                sort_by_dict['field'] = 'TOP_SELLERS'
                sort_by_dict['order'] = 'DESC'
            elif 'price_low_to_high' in sort_by:
                sort_by_dict['field'] = 'PRICE'
                sort_by_dict['order'] = 'ASC'
            elif 'price_high_to_low' in sort_by:
                sort_by_dict['field'] = 'PRICE'
                sort_by_dict['order'] = 'DESC'
            elif 'top_related_product' in sort_by:
                sort_by_dict['field'] = 'TOP_RATED'
                sort_by_dict['order'] = 'ASC'
            elif 'best_match' in sort_by:
                sort_by_dict['field'] = 'BEST_MATCH'
                sort_by_dict['order'] = 'ASC'

        print(sort_by_dict)

        # {field: "PRICE", order: "DESC"}
        payload = json.dumps({
            "operationName": "searchModel",
            "variables": {
                "skipInstallServices": False,
                "skipKPF": False,
                "skipSpecificationGroup": False,
                "skipSubscribeAndSave": False,
                "storefilter": "ALL",
                "channel": "DESKTOP",
                "additionalSearchParams": {
                    "mcvisId": "47724937741940748334163300878188542571",
                    "deliveryZip": "96913",
                    "multiStoreIds": []
                },
                "filter": {},
                "keyword": keyword,
                "navParam": None,
                "orderBy": sort_by_dict,
                "pageSize": 24,
                "startIndex": int(startIndex),
                "storeId": "1710"
            },
            "query": "query searchModel($storeId: String, $zipCode: String, $skipInstallServices: Boolean = true, $startIndex: Int, $pageSize: Int, $orderBy: ProductSort, $filter: ProductFilter, $skipKPF: Boolean = false, $skipSpecificationGroup: Boolean = false, $skipSubscribeAndSave: Boolean = false, $keyword: String, $navParam: String, $storefilter: StoreFilter = ALL, $itemIds: [String], $channel: Channel = DESKTOP, $additionalSearchParams: AdditionalParams, $loyaltyMembershipInput: LoyaltyMembershipInput) {\n  searchModel(keyword: $keyword, navParam: $navParam, storefilter: $storefilter, storeId: $storeId, itemIds: $itemIds, channel: $channel, additionalSearchParams: $additionalSearchParams, loyaltyMembershipInput: $loyaltyMembershipInput) {\n    metadata {\n      hasPLPBanner\n      categoryID\n      analytics {\n        semanticTokens\n        dynamicLCA\n        __typename\n      }\n      canonicalUrl\n      searchRedirect\n      clearAllRefinementsURL\n      contentType\n      h1Tag\n      isStoreDisplay\n      productCount {\n        inStore\n        __typename\n      }\n      stores {\n        storeId\n        storeName\n        address {\n          postalCode\n          __typename\n        }\n        nearByStores {\n          storeId\n          storeName\n          distance\n          address {\n            postalCode\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    products(startIndex: $startIndex, pageSize: $pageSize, orderBy: $orderBy, filter: $filter) {\n      identifiers {\n        storeSkuNumber\n        specialOrderSku\n        canonicalUrl\n        brandName\n        itemId\n        productLabel\n        modelNumber\n        productType\n        parentId\n        isSuperSku\n        __typename\n      }\n      installServices(storeId: $storeId, zipCode: $zipCode) @skip(if: $skipInstallServices) {\n        scheduleAMeasure @skip(if: $skipInstallServices)\n        gccCarpetDesignAndOrderEligible @skip(if: $skipInstallServices)\n        __typename\n      }\n      itemId\n      dataSources\n      media {\n        images {\n          url\n          type\n          subType\n          sizes\n          __typename\n        }\n        __typename\n      }\n      pricing(storeId: $storeId) {\n        value\n        alternatePriceDisplay\n        alternate {\n          bulk {\n            pricePerUnit\n            thresholdQuantity\n            value\n            __typename\n          }\n          unit {\n            caseUnitOfMeasure\n            unitsOriginalPrice\n            unitsPerCase\n            value\n            __typename\n          }\n          __typename\n        }\n        original\n        mapAboveOriginalPrice\n        message\n        preferredPriceFlag\n        promotion {\n          type\n          description {\n            shortDesc\n            longDesc\n            __typename\n          }\n          dollarOff\n          percentageOff\n          savingsCenter\n          savingsCenterPromos\n          specialBuySavings\n          specialBuyDollarOff\n          specialBuyPercentageOff\n          dates {\n            start\n            end\n            __typename\n          }\n          promotionTag\n          __typename\n        }\n        specialBuy\n        unitOfMeasure\n        __typename\n      }\n      reviews {\n        ratingsReviews {\n          averageRating\n          totalReviews\n          __typename\n        }\n        __typename\n      }\n      availabilityType {\n        discontinued\n        type\n        buyable\n        status\n        __typename\n      }\n      badges(storeId: $storeId) {\n        name\n        label\n        __typename\n      }\n      details {\n        collection {\n          collectionId\n          name\n          url\n          __typename\n        }\n        highlights\n        installation {\n          serviceType\n          __typename\n        }\n        __typename\n      }\n      favoriteDetail {\n        count\n        __typename\n      }\n      fulfillment(storeId: $storeId, zipCode: $zipCode) {\n        backordered\n        backorderedShipDate\n        bossExcludedShipStates\n        excludedShipStates\n        seasonStatusEligible\n        fulfillmentOptions {\n          type\n          fulfillable\n          services {\n            type\n            hasFreeShipping\n            freeDeliveryThreshold\n            locations {\n              curbsidePickupFlag\n              isBuyInStoreCheckNearBy\n              distance\n              inventory {\n                isOutOfStock\n                isInStock\n                isLimitedQuantity\n                isUnavailable\n                quantity\n                maxAllowedBopisQty\n                minAllowedBopisQty\n                __typename\n              }\n              isAnchor\n              locationId\n              storeName\n              state\n              type\n              storePhone\n              __typename\n            }\n            deliveryTimeline\n            deliveryDates {\n              startDate\n              endDate\n              __typename\n            }\n            deliveryCharge\n            dynamicEta {\n              hours\n              minutes\n              __typename\n            }\n            totalCharge\n            __typename\n          }\n          __typename\n        }\n        anchorStoreStatus\n        anchorStoreStatusType\n        onlineStoreStatus\n        onlineStoreStatusType\n        __typename\n      }\n      info {\n        hasSubscription\n        isBuryProduct\n        isSponsored\n        isGenericProduct\n        isLiveGoodsProduct\n        sponsoredBeacon {\n          onClickBeacon\n          onViewBeacon\n          onClickBeacons\n          onViewBeacons\n          __typename\n        }\n        sponsoredMetadata {\n          campaignId\n          placementId\n          slotId\n          sponsoredId\n          trackSource\n          __typename\n        }\n        globalCustomConfigurator {\n          customExperience\n          __typename\n        }\n        returnable\n        hidePrice\n        productSubType {\n          name\n          link\n          __typename\n        }\n        categoryHierarchy\n        samplesAvailable\n        customerSignal {\n          previouslyPurchased\n          __typename\n        }\n        productDepartmentId\n        productDepartment\n        augmentedReality\n        ecoRebate\n        quantityLimit\n        sskMin\n        sskMax\n        unitOfMeasureCoverage\n        wasMaxPriceRange\n        wasMinPriceRange\n        swatches {\n          isSelected\n          itemId\n          label\n          swatchImgUrl\n          url\n          value\n          __typename\n        }\n        totalNumberOfOptions\n        paintBrand\n        dotComColorEligible\n        classNumber\n        __typename\n      }\n      keyProductFeatures @skip(if: $skipKPF) {\n        keyProductFeaturesItems {\n          features {\n            name\n            refinementId\n            refinementUrl\n            value\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      specificationGroup @skip(if: $skipSpecificationGroup) {\n        specifications {\n          specName\n          specValue\n          __typename\n        }\n        specTitle @skip(if: $skipSpecificationGroup)\n        __typename\n      }\n      subscription @skip(if: $skipSubscribeAndSave) {\n        defaultfrequency @skip(if: $skipSubscribeAndSave)\n        discountPercentage @skip(if: $skipSubscribeAndSave)\n        subscriptionEnabled @skip(if: $skipSubscribeAndSave)\n        __typename\n      }\n      sizeAndFitDetail {\n        attributeGroups {\n          attributes {\n            attributeName\n            dimensions\n            __typename\n          }\n          dimensionLabel\n          productType\n          __typename\n        }\n        __typename\n      }\n      dataSource\n      __typename\n    }\n    id\n    searchReport {\n      totalProducts\n      didYouMean\n      correctedKeyword\n      keyword\n      pageSize\n      searchUrl\n      sortBy\n      sortOrder\n      startIndex\n      __typename\n    }\n    relatedResults {\n      universalSearch {\n        title\n        __typename\n      }\n      relatedServices {\n        label\n        __typename\n      }\n      visualNavs {\n        label\n        imageId\n        webUrl\n        categoryId\n        imageURL\n        __typename\n      }\n      visualNavContainsEvents\n      relatedKeywords {\n        keyword\n        __typename\n      }\n      __typename\n    }\n    taxonomy {\n      brandLinkUrl\n      breadCrumbs {\n        browseUrl\n        creativeIconUrl\n        deselectUrl\n        dimensionId\n        dimensionName\n        label\n        refinementKey\n        url\n        __typename\n      }\n      __typename\n    }\n    templates\n    partialTemplates\n    dimensions {\n      label\n      refinements {\n        refinementKey\n        label\n        recordCount\n        selected\n        imgUrl\n        url\n        nestedRefinements {\n          label\n          url\n          recordCount\n          refinementKey\n          __typename\n        }\n        __typename\n      }\n      collapse\n      dimensionId\n      isVisualNav\n      isVisualDimension\n      isNumericFilter\n      isColorSwatch\n      nestedRefinementsLimit\n      visualNavSequence\n      __typename\n    }\n    orangeGraph {\n      universalSearchArray {\n        pods {\n          title\n          description\n          imageUrl\n          link\n          isProContent\n          recordType\n          __typename\n        }\n        info {\n          title\n          __typename\n        }\n        __typename\n      }\n      productTypes\n      intents\n      orderNumber\n      __typename\n    }\n    appliedDimensions {\n      label\n      refinements {\n        label\n        refinementKey\n        url\n        __typename\n      }\n      isNumericFilter\n      __typename\n    }\n    primaryFilters {\n      collapse\n      dimensionId\n      isVisualNav\n      isVisualDimension\n      isNumericFilter\n      isColorSwatch\n      label\n      nestedRefinementsLimit\n      refinements {\n        label\n        refinementKey\n        recordCount\n        selected\n        imgUrl\n        url\n        nestedRefinements {\n          label\n          url\n          recordCount\n          refinementKey\n          __typename\n        }\n        __typename\n      }\n      visualNavSequence\n      __typename\n    }\n    __typename\n  }\n}\n"
        })
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
            'Apollographql-Client-Name': 'general-merchandise',
            'Apollographql-Client-Version': '0.0.0',
            'Content-Type': 'application/json',
            'Origin': 'https://www.homedepot.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            'X-Api-Cookies': '{"x-user-id":"02065667-2283-ead7-cadc-ca62c75c8dce"}',
            'X-Current-Url': f'/s/{keyword}',
            'X-Experience-Name': 'general-merchandise',
            'X-Hd-Dc': 'origin',
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code != 200:
           for i in range(5):
               response = requests.request("POST", url, headers=headers, data=payload)
               if response.status_code == 200:
                   break
        json_data = response.json()


        product_list = json_data['data']['searchModel']['products']

        search_products = list()
        for product in product_list:
            sponsored = product['info']['isSponsored']
            if sponsored != True:
                item = dict()
                try:canonicalUrl = f"https://www.homedepot.com{product['identifiers']['canonicalUrl']}"
                except:canonicalUrl = None
                try:brandName = product['identifiers']['brandName']
                except:brandName = None
                try:itemId = product['identifiers']['itemId']
                except:itemId = None
                try:productLabel = product['identifiers']['productLabel']
                except:productLabel = None
                try:modelNumber = product['identifiers']['modelNumber']
                except:modelNumber = None
                try:productType = product['identifiers']['productType']
                except:productType = None
                try:product_images = list(img['url'].replace("<SIZE>", "600") for img in product['media']['images'])
                except:product_images = None
                try:price = product['pricing']['original']
                except:price = None
                try:unitOfMeasure = product['pricing']['unitOfMeasure']
                except:unitOfMeasure = None
                try:averageRating = round(float(product['reviews']['ratingsReviews']['averageRating']), 2)
                except:averageRating = None
                try:totalReviews = product['reviews']['ratingsReviews']['totalReviews']
                except:totalReviews = None

                item['canonicalUrl'] = canonicalUrl
                item['brandName'] = brandName
                item['itemId'] = itemId
                item['productLabel'] = productLabel
                item['modelNumber'] = modelNumber
                item['productType'] = productType
                item['product_images'] = product_images
                item['price'] = price
                item['unitOfMeasure'] = unitOfMeasure
                item['averageRating'] = averageRating
                item['totalReviews'] = totalReviews

                search_products.append(item)
        response_json['results'] = search_products
        return JsonResponse(response_json)
    else:
        response_json['failure'] = "invalid request type"
        return JsonResponse(response_json)

def search_by_product(request):
    item = dict()
    try:itemid = request.GET['item_id']
    except:itemid = ''
    print(request.GET)
    if itemid == '' or 'item_id' not in request.GET:
        item['result'] = "please enter valid item id"
        return JsonResponse(item)

    url = "https://www.homedepot.com/federation-gateway/graphql?opname=productClientOnlyProduct"

    headers = {
        'accept': '*/*',
        # 'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,de;q=0.8',
        'apollographql-client-name': 'general-merchandise',
        'apollographql-client-version': '0.0.0',
        'cookie': 'THD_CACHE_NAV_PERSIST=; _pxvid=2061df16-c879-11ed-ba85-756863445462; thda.u=b2d7638a-da69-198e-1d11-63340ca840c9; _px_f394gi7Fvmc43dfg_user_id=MjI1M2FhZTAtYzg3OS0xMWVkLWI2ZDQtOWRhMzQ2M2M0ZmZm; ajs_anonymous_id=c0e3b701-49c5-4c27-a264-b90dfd033058; _meta_googleGtag_ga_library_loaded=1679465814797; _meta_facebookPixel_beaconFired=1679465814822; _meta_bing_beaconFired=1679465814825; _meta_neustar_mcvisid=38377620302924306582728779248102172617; _meta_metarouter_timezone_offset=-330; aam_mobile=seg%3D1131078; aam_uuid=38295075346162813992718431101728442812; _meta_amobee_uid=7126775527081979917; _meta_yahooMedia_yahoo_id=y-qtCCFstE2r1u5YcSgLQESuJ1qXIPLzDfM3JZ~A; _meta_revjet_revjet_vid=4759495595770943657; trx=4759495595770943657; _meta_acuityAds_auid=757754565272; _meta_acuityAds_cauid=auid=757754565272; _meta_tapAd_id=16039e5d-d71a-4bb4-aa13-3c1a52e5e37e; _meta_inMarket_userNdat=D48C4F2D569D1A647622210502FC893A; _meta_mediaMath_mm_id=896c63f8-b823-4300-97c1-432b4d904477; _meta_mediaMath_cid=896c63f8-b823-4300-97c1-432b4d904477; _gcl_au=1.1.222607780.1679465816; _meta_neustar_fabrickId=E1:TZuh3_DugzLwb8Iddrw5DXStx6qHkwEZa4BQ5VZcjRGrpoCWXpa49BKSdAnzRloxoukuQ_pVP6AVdUcT-NAdF0AkbTCzZD4ysfWOrU61IqU; _meta_neustar_tuid=210750604441002134527; _ga=GA1.1.1561832489.1679465814; QuantumMetricUserID=0d7769e88385c31dceae869e658cbc4a; LPVID=ZhYTZmNTVlMTZjZmQ3Y2Mx; DELIVERY_ZIP_TYPE=USER; _ga_9H2R4ZXG4J=GS1.1.1679465816.1.1.1679465839.37.0.0; _meta_adobe_aam_uuid=38295075346162813992718431101728442812; _meta_adobe_neustar=1679465844597; _meta_adobe_google=1679465844598; _meta_adobe_microsoft=1679465844600; _meta_neustar_aam=38295075346162813992718431101728442812; _meta_adobe_fire={"xandr":false,"revjet":true,"mediaMath":true}; _meta_googleGtag_ga=GA1.1.1561832489.1679465814; _meta_mediaMath_iframe_counter=5; QSI_SI_2lVW226zFt4dVJ3_intercept=true; _meta_pinterest_pin-unauth=dWlkPU9XTm1OR1kxWmpndE1EbGhOaTAwWVRJekxXSXpPVEl0WlRGa1lqWXpZamcxTlRabA; cart_activity=e9a0dcc7-541d-4808-ae95-949885148568; THD_PERSIST=C6%3d%7b%22I1%22%3a%221%22%7d%3a%3bC6%5fEXP%3d1682241162; DELIVERY_ZIP=95380; THD_NR=1; _meta_movableInk_mi_u=c0e3b701-49c5-4c27-a264-b90dfd033058; _abck=BF6AA3AA0014332F42F71D7922AB8D2A~0~YAAQxydzaJb7VQeHAQAAqM6xJglcb+g/4X8xF5i/v3OdhfvgpF4sC2wTqln4F6c8HU/dy7KK7Be7Cp2c4LRAsoewBImrZJgqANNSqivDKNeMh8ieSQehotCn/ooIbFx6zKBd0zmVSihlyPJzAukh2xLzUJqpvzObwDzfn4i+9x5zCnL9BQKM+JbAypXGmTGzgWOQ5Gwfj66+1Ll1290jwTt2saQIDE0ggleIDVLK8IBvpgZ6+7kQ8DmfzJhd1Kwt85Olcbp6f14sTxGv03P+aaQE7yg7bc2Xh23Lm5MR5mVdjCAvjUfuu0k6YSbDZWXnAHKzGlUkkinHWCaTbbMx6pnDj0ju1F6CBA1EChi/CWEg1z3ClSYmDgKMLAdjGlJKyT05eAXQeoT8IlRfkWE2dG4v9BpOuDc2PoVJ~-1~-1~-1; AKA_A2=A; bm_sz=72283115AEF2456182C8066F643C9488~YAAQfidzaMA9hQ+HAQAA5AiDJxMWGOkkLNcy/IvAYncOv+1v2Oq9P1O6s7gzHCEVw6KEOZw9WfcWR87lLe8lEygs1mgsfdRauQmwtopTZG7QR9Pm8Jk5MScAeh1jv8XGXmt4x2xnFxFV7xOo32V0oJ+ePiVOVWRaSdsfCqlOLx0YTA0207PrkjCDeOtSmtXvkjySQlL4VZb0lA+j1HMuc0uzJmxHpNsRJqbMvW8cO2/UsU/pSqMeJ0d4Yd5A5JUC6csMnq99Rkmkfg2h3ng8U30/t/iqbqFlzDj9YSpdqr3OF4c676MZH27UK+msAsdeMF0ibfh9LHWhc6xDCAs=~4604228~3356721; THD_SESSION=; THD_CACHE_NAV_SESSION=; ak_bmsc=583E5E960F99C096525F674981601803~000000000000000000000000000000~YAAQfidzaNM9hQ+HAQAAihCDJxOSKuUWMNweBiDPrFyLwNxr+XwIoYitJz52kHAz+/WYaji34HAXJGN1jLoa976RN+Eyj74eZ+SxtY1de+Ha8yekuLgiR9x1+QPSMFOtFX8csRUmKMwWq4kTt9FmFDrQLcesEys5/rN2o5Xyj1qU1uX4RxGrbbbLAUrB65BV1Zz6Iy8x5l57twWmQjTA9HJvSy9tKnrA4pRLt+3aiNK+YaapLz/pLHAUCFpPuapVJ2fFA5vZmAfI2OGnVlvZbmwRJF7jLeFgK2Rhh8dV+y6O6MLYY45YT0jjn+SIshxHif3xBA17pduSFlRCSX83XQcJ5gIxjkRLpEFoa/O4D3Hslc82LYzOZl5Rex0Ol5i256/Am3LsqLdP130SB0POdk8zuroyLD5FwI4eJVr1VdhPezyB7mNPk7IhvMOcJuIjEWGJjwZDNR284+FKNsmLL7fVRKLkpoQN+yfKMRL2mKEdODcmPWpTWpuGk8S8MdA=; QuantumMetricSessionID=6d6a6fbfe186f4c6859c8d0d89d3d8b6; HD_DC=origin; akacd_usbeta=3857448304~rv=65~id=4d3e8565bf88ba1f8db495cc7f58dad4; at_check=true; IN_STORE_API_SESSION=TRUE; thda.s=f467bd8f-e0c4-0e1b-7af4-adb3b91535f6; THD_LOCALIZER=%7B%22WORKFLOW%22%3A%22GEO_LOCATION%22%2C%22THD_FORCE_LOC%22%3A%221%22%2C%22THD_INTERNAL%22%3A%220%22%2C%22THD_LOCSTORE%22%3A%221710%2BGuam%20-%20Tamuning%20-%20Tamuning%2C%20GU%2B%22%2C%22THD_STRFINDERZIP%22%3A%2296913%22%2C%22THD_STORE_HOURS%22%3A%221%3B7%3A00-20%3A00%3B2%3B6%3A00-22%3A00%3B3%3B6%3A00-22%3A00%3B4%3B6%3A00-22%3A00%3B5%3B6%3A00-22%3A00%3B6%3B6%3A00-22%3A00%3B7%3B6%3A00-22%3A00%22%2C%22THD_STORE_HOURS_EXPIRY%22%3A1679999111%7D; QSI_HistorySession=https%3A%2F%2Fwww.homedepot.com%2Fp%2FPool-Time-Chlorinating-MAXBlue-25-lbs-3-in-Tablets-22825PTM%2F302895488~1679995515203; AMCVS_F6421253512D2C100A490D45%40AdobeOrg=1; AMCV_F6421253512D2C100A490D45%40AdobeOrg=1585540135%7CMCMID%7C38377620302924306582728779248102172617%7CMCAAMLH-1680600315%7C12%7CMCAAMB-1680600315%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1680002716s%7CNONE%7CMCCIDH%7C1158480622%7CvVersion%7C4.4.0; _meta_metarouter_sessionID=1679995516159; thda.m=38377620302924306582728779248102172617; _meta_pinterest_derived_epik_failure=not found; _px=wjUTa2EguoeZ5Uge7ozLdK2JqoCWqmwDgLVOFYhgqf4oOIwRKXqKt+0gtNJUTcBCeNd6TMfVTr/j+NZ2BXtjdw==:1000:qG/rE5UoUvJbXm6oVn+XBmvwquTQ62tkhgREJOBBeB/hu5KyB+4NvLPwV9GzLBFu6e09VKRcEXvptM5mxFGztkcDTkTE/nfHCV2v0W3huqYaqx3BAjyekS6BfHl05ipqh0fQP0YMoCnK3bFBxNrFKKofhtEFX1UeKpcFRjnTZsjlUBiam4gon0RgbArxXvQE+eontwM5LpKd7RfsTcru1aLod9sp7BhGPZsLSt1pjs7yag3hTcQn35y/AuFhkQHEgwsetLTI1SOUtHlMTNyV0A==; forterToken=d53723c5f171450c988ee5eb9badf6f4_1679995532467__UDF43_13ck; s_pers=%20productnum%3D3%7C1682240868753%3B%20s_nr365%3D1679995533878-Repeat%7C1711531533878%3B%20s_dslv%3D1679995533888%7C1774603533888%3B; s_sess=%20s_pv_pName%3Dproductdetails%253E302895488%3B%20s_pv_pType%3Dpip%3B%20s_pv_cmpgn%3D%3B%20s_pv_pVer%3D%3B%20stsh%3D%3B%20s_cc%3Dtrue%3B; akavpau_prod=1679995838~id=96b529b8535159d22273b6856b406e0b; mbox=PC#0c5357b973aa4270a7be9a474b0dd0ac.31_0#1743240324|session#471cf7a5502244928de12095b686896e#1679997401; RT="z=1&dm=www.homedepot.com&si=28fdd348-e921-491a-b964-15d0074d1f00&ss=lfs1powr&sl=2&tt=4wy&obo=1&rl=1"; _pxde=b7f8a84f099b522a85153aac362c2f32f6ed3695f2405cdc86f584f3c23e8650:eyJ0aW1lc3RhbXAiOjE2Nzk5OTU1NDAwOTN9; HD_DC=origin; _abck=BF6AA3AA0014332F42F71D7922AB8D2A~-1~YAAQXidzaPhPYyOHAQAAxwfDJwkLQPuaumhbdRbRqwcCO5Vm4Tfa976e0sozvCMK8fpU6K3OqrAYxk0YNsUVs9WHDbIJy+vTbbDgOxyJJWjsTeRg/JecuHziKQxyKioqt78wcwbaCta5NyvN71BuLCPJn0QpjuL+X7d5NWTUM4wLIinLS1SCAIn4JJjJmv2KR9WkwsOW/dC5Fpmg7zEO0pWnvu0sua8zFJKMWnHfW4qdz2ZBWafSuVo+pf4UFjANtqSqD/Lr4D/xgaRekGtGwTWN6DLh0qmR7zWyjOZ2pfa57hk6oZ6rVU1YCVgOjVwvqZEAnj6oR9voeMxVde5n8itl0zkHp3qQ+5sow9pHzceh8Ovp9znz7JfxHH8s962irw==~0~-1~-1; ak_bmsc=26A6860BCEAA0F47BB778C2844D47C10~000000000000000000000000000000~YAAQDR0gF9OtSiSHAQAA8IGVJxOgIbu+h+uPGhOZy6Pc38r9oqtj9U3ZbhC3vAG4QAHDIYbasdMth0oJHcBhspdYINRJOq2vw7ft7j19/AMT5km4TVmiLywSJ2RSbSyqv07Hzq4KEHhlgSBcw5Z+7FtDvu48ObxuJdoiuLjkwDzHBejbVSBFxQZuYJOmkpyLTbLrH157zwYpwjKfAk5IrAkDrJ2PVOkvxiwk6wDdHjo78hx/quik/u34Gk3lv0Nm0UCNC+C1VN2eyQksTHjKfSjI3GrEk0kh8gNU+vmGtmBXdjVg9bZrCQpaBdXT6v76HPkGNHOFvPXTpR3UDiH5ui3+O6PJuiAYniruGl2q2b+fRX7UAFcxuZiLcDtNcq4r; bm_sz=FA986F6DFFFD3954CFC4257EE0F6D0B8~YAAQDR0gF7qMRySHAQAABhlqJxNQixFUFaOpozqtOOji65bZ39l8AoJc+eJLflRfACd6M+x9JWIARJ8nRq6n0LR4qxapswuy8UDONjvZF7tnYILblA7WKGpgV4eC/jEf7Z5d9nqJmf6wNzDSc7GIv+X2usXG7eRaOmUDnDDoVd9at+wrnXUAo8Biaa3D1ViLbXPdCdfuDTA+WILqmRUICLngfq30FOiOqYoBL3hwpv2P9eXs3ZOv+p0W+VNeDMXLhqsqLS7MT/AITkEpMiynmkEkikRD0tKaaasYZOMKWj4VxaTt4LK42YLwfQnrBwUUQX2bMDkombub4P/Ibn0=~4599864~3686980; akacd_usbeta=3857432746~rv=82~id=7bdad1bb1b72cb2491b78d6e2b67191f',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'x-api-cookies': '{"x-user-id":"b2d7638a-da69-198e-1d11-63340ca840c9"}',
        'x-debug': 'false',
        'x-experience-name': 'general-merchandise',
        'x-hd-dc': 'origin',
        'referer': 'https://www.google.com',
        'Content-Type': 'application/json'
    }

    payload = json.dumps({
        "operationName": "productClientOnlyProduct",
        "variables": {
            "skipSpecificationGroup": False,
            "skipSubscribeAndSave": False,
            "skipInstallServices": True,
            "skipKPF": False,
            "itemId": f'{itemid}',
            "storeId": '940',
            "zipCode": "96913"
        },
        "query": "query productClientOnlyProduct($storeId: String, $zipCode: String, $quantity: Int, $itemId: String!, $dataSource: String, $loyaltyMembershipInput: LoyaltyMembershipInput, $skipSpecificationGroup: Boolean = false, $skipSubscribeAndSave: Boolean = false, $skipInstallServices: Boolean = true, $skipKPF: Boolean = false) {\n  product(itemId: $itemId, dataSource: $dataSource, loyaltyMembershipInput: $loyaltyMembershipInput) {\n    fulfillment(storeId: $storeId, zipCode: $zipCode, quantity: $quantity) {\n      backordered\n      fulfillmentOptions {\n        type\n        services {\n          type\n          hasFreeShipping\n          freeDeliveryThreshold\n          locations {\n            curbsidePickupFlag\n            isBuyInStoreCheckNearBy\n            distance\n            inventory {\n              isOutOfStock\n              isInStock\n              isLimitedQuantity\n              isUnavailable\n              quantity\n              maxAllowedBopisQty\n              minAllowedBopisQty\n              __typename\n            }\n            isAnchor\n            locationId\n            storeName\n            state\n            type\n            storePhone\n            __typename\n          }\n          optimalFulfillment\n          deliveryTimeline\n          deliveryDates {\n            startDate\n            endDate\n            __typename\n          }\n          deliveryCharge\n          dynamicEta {\n            hours\n            minutes\n            __typename\n          }\n          totalCharge\n          __typename\n        }\n        fulfillable\n        __typename\n      }\n      backorderedShipDate\n      bossExcludedShipStates\n      excludedShipStates\n      seasonStatusEligible\n      anchorStoreStatus\n      anchorStoreStatusType\n      fallbackMode\n      sthExcludedShipState\n      bossExcludedShipState\n      onlineStoreStatus\n      onlineStoreStatusType\n      inStoreAssemblyEligible\n      __typename\n    }\n    info {\n      dotComColorEligible\n      hidePrice\n      ecoRebate\n      quantityLimit\n      sskMin\n      sskMax\n      unitOfMeasureCoverage\n      wasMaxPriceRange\n      wasMinPriceRange\n      productSubType {\n        name\n        link\n        __typename\n      }\n      fiscalYear\n      productDepartment\n      classNumber\n      forProfessionalUseOnly\n      globalCustomConfigurator {\n        customButtonText\n        customDescription\n        customExperience\n        customExperienceUrl\n        customTitle\n        __typename\n      }\n      paintBrand\n      movingCalculatorEligible\n      label\n      hasSubscription\n      isBuryProduct\n      isSponsored\n      isGenericProduct\n      isLiveGoodsProduct\n      sponsoredBeacon {\n        onClickBeacon\n        onViewBeacon\n        __typename\n      }\n      sponsoredMetadata {\n        campaignId\n        placementId\n        slotId\n        __typename\n      }\n      returnable\n      categoryHierarchy\n      samplesAvailable\n      customerSignal {\n        previouslyPurchased\n        __typename\n      }\n      productDepartmentId\n      augmentedReality\n      swatches {\n        isSelected\n        itemId\n        label\n        swatchImgUrl\n        url\n        value\n        __typename\n      }\n      totalNumberOfOptions\n      gccExperienceOmsId\n      recommendationFlags {\n        visualNavigation\n        pipCollections\n        packages\n        ACC\n        frequentlyBoughtTogether\n        bundles\n        __typename\n      }\n      replacementOMSID\n      minimumOrderQuantity\n      projectCalculatorEligible\n      subClassNumber\n      calculatorType\n      pipCalculator {\n        coverageUnits\n        display\n        publisher\n        toggle\n        __typename\n      }\n      protectionPlanSku\n      hasServiceAddOns\n      consultationType\n      __typename\n    }\n    identifiers {\n      skuClassification\n      canonicalUrl\n      brandName\n      itemId\n      modelNumber\n      productLabel\n      storeSkuNumber\n      upcGtin13\n      specialOrderSku\n      toolRentalSkuNumber\n      rentalCategory\n      rentalSubCategory\n      upc\n      productType\n      isSuperSku\n      parentId\n      roomVOEnabled\n      sampleId\n      __typename\n    }\n    itemId\n    dataSources\n    availabilityType {\n      discontinued\n      status\n      type\n      buyable\n      __typename\n    }\n    details {\n      description\n      collection {\n        url\n        collectionId\n        name\n        __typename\n      }\n      highlights\n      installation {\n        leadGenUrl\n        __typename\n      }\n      __typename\n    }\n    media {\n      images {\n        url\n        type\n        subType\n        sizes\n        altText\n        __typename\n      }\n      video {\n        shortDescription\n        thumbnail\n        url\n        videoStill\n        link {\n          text\n          url\n          __typename\n        }\n        title\n        type\n        videoId\n        longDescription\n        __typename\n      }\n      threeSixty {\n        id\n        url\n        __typename\n      }\n      augmentedRealityLink {\n        usdz\n        image\n        __typename\n      }\n      __typename\n    }\n    pricing(storeId: $storeId) {\n      promotion {\n        dates {\n          end\n          start\n          __typename\n        }\n        type\n        description {\n          shortDesc\n          longDesc\n          __typename\n        }\n        dollarOff\n        percentageOff\n        promotionTag\n        savingsCenter\n        savingsCenterPromos\n        specialBuySavings\n        specialBuyDollarOff\n        specialBuyPercentageOff\n        experienceTag\n        subExperienceTag\n        itemList\n        reward {\n          tiers {\n            minPurchaseAmount\n            minPurchaseQuantity\n            rewardPercent\n            rewardAmountPerOrder\n            rewardAmountPerItem\n            rewardFixedPrice\n            __typename\n          }\n          __typename\n        }\n        nvalues\n        brandRefinementId\n        __typename\n      }\n      value\n      alternatePriceDisplay\n      alternate {\n        bulk {\n          pricePerUnit\n          thresholdQuantity\n          value\n          __typename\n        }\n        unit {\n          caseUnitOfMeasure\n          unitsOriginalPrice\n          unitsPerCase\n          value\n          __typename\n        }\n        __typename\n      }\n      original\n      mapAboveOriginalPrice\n      message\n      preferredPriceFlag\n      specialBuy\n      unitOfMeasure\n      conditionalPromotions {\n        dates {\n          start\n          end\n          __typename\n        }\n        description {\n          shortDesc\n          longDesc\n          __typename\n        }\n        experienceTag\n        subExperienceTag\n        eligibilityCriteria {\n          itemGroup\n          minPurchaseAmount\n          minPurchaseQuantity\n          relatedSkusCount\n          omsSkus\n          __typename\n        }\n        reward {\n          tiers {\n            minPurchaseAmount\n            minPurchaseQuantity\n            rewardPercent\n            rewardAmountPerOrder\n            rewardAmountPerItem\n            rewardFixedPrice\n            __typename\n          }\n          __typename\n        }\n        nvalues\n        brandRefinementId\n        __typename\n      }\n      __typename\n    }\n    reviews {\n      ratingsReviews {\n        averageRating\n        totalReviews\n        __typename\n      }\n      __typename\n    }\n    seo {\n      seoKeywords\n      seoDescription\n      __typename\n    }\n    specificationGroup @skip(if: $skipSpecificationGroup) {\n      specifications {\n        specName\n        specValue\n        __typename\n      }\n      specTitle @skip(if: $skipSpecificationGroup)\n      __typename\n    }\n    taxonomy {\n      breadCrumbs {\n        label\n        url\n        browseUrl\n        creativeIconUrl\n        deselectUrl\n        dimensionName\n        refinementKey\n        __typename\n      }\n      brandLinkUrl\n      __typename\n    }\n    favoriteDetail {\n      count\n      __typename\n    }\n    sizeAndFitDetail {\n      attributeGroups {\n        attributes {\n          attributeName\n          dimensions\n          __typename\n        }\n        dimensionLabel\n        productType\n        __typename\n      }\n      __typename\n    }\n    subscription @skip(if: $skipSubscribeAndSave) {\n      defaultfrequency @skip(if: $skipSubscribeAndSave)\n      discountPercentage @skip(if: $skipSubscribeAndSave)\n      subscriptionEnabled @skip(if: $skipSubscribeAndSave)\n      __typename\n    }\n    badges(storeId: $storeId) {\n      label\n      name\n      color\n      creativeImageUrl\n      endDate\n      message\n      timerDuration\n      timer {\n        timeBombThreshold\n        daysLeftThreshold\n        dateDisplayThreshold\n        message\n        __typename\n      }\n      __typename\n    }\n    dataSource\n    installServices(storeId: $storeId, zipCode: $zipCode) @skip(if: $skipInstallServices) {\n      scheduleAMeasure @skip(if: $skipInstallServices)\n      gccCarpetDesignAndOrderEligible @skip(if: $skipInstallServices)\n      __typename\n    }\n    keyProductFeatures @skip(if: $skipKPF) {\n      keyProductFeaturesItems {\n        features {\n          name\n          refinementId\n          refinementUrl\n          value\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    projectDetails {\n      projectId\n      __typename\n    }\n    seoDescription\n    __typename\n  }\n}\n"
    })

    response = requests.request("POST", url, headers=headers, data=payload)

    json_data = response.json()
    # print(json_data)

    main_json_data = json_data['data']['product']
    # print(main_json_data)

    try:
        product_url = 'https://www.homedepot.com' + main_json_data['identifiers']['canonicalUrl']
    except Exception as e:
        product_url = ''
        print("Error in product_url . . . . . . . . ", e)

    print(product_url)
    try:
        product_name = main_json_data['identifiers']['productLabel']
    except Exception as e:
        product_name = ''
        print("Error in product_name . . . . . . . . ", e)

    print(product_name)
    try:
        brand_name = main_json_data['identifiers']['brandName']
    except Exception as e:
        brand_name = ''
        print("Error in brand_name . . . . . . . . ", e)

    try:
        MPN = main_json_data['identifiers']['modelNumber']
    except Exception as e:
        MPN = ''
        print("Error in MPN . . . . . . . . ", e)

    try:
        SKU = main_json_data['identifiers']['storeSkuNumber']
    except Exception as e:
        SKU = ''
        print("Error in SKU . . . . . . . . ", e)

    try:
        value = main_json_data['pricing']['value']
        original = main_json_data['pricing']['original']

        if original is None:
            MRP = value
            offer_price = ''
        else:
            offer_price = value
            MRP = original
    except Exception as e:
        MRP = ''
        offer_price = ''
        print("Error in MRP . . . . . . . . ", e)

    try:
        variantls = main_json_data['specificationGroup']
    except:
        variantls = []

    variant = ''
    Unit_of_Measure = ''

    if variantls != []:
        for min in variantls:
            for spec in min['specifications']:
                specName = spec['specName']
                if specName == "Product Weight (lb.)":
                    variant_one = spec['specValue']
                    if " " in variant_one:
                        variant = str(variant_one).split(" ")[0].replace(".", "")
                        Unit_of_Measure = str(variant_one).split(" ")[1]
                    else:
                        variant = variant_one
                        Unit_of_Measure = ''
    else:
        variant = ''
        Unit_of_Measure = ''

    try:
        star_rating = float(main_json_data['reviews']['ratingsReviews']['averageRating'])
        star_rating = round(star_rating, 1)
    except:
        star_rating = ''
    try:
        reviews_count = main_json_data['reviews']['ratingsReviews']['totalReviews']
    except:
        reviews_count = ''
    try:
        description = main_json_data['details']['description']
    except:
        description = ''

    try:
        stock = main_json_data['fulfillment']['fulfillmentOptions']
        if stock == None:
            stock = 'No'
        else:
            stock = 'Yes'
    except:
        stock = 'No'

    try:
        all_dict = {}
        temp_pro_specification = main_json_data['specificationGroup']
        for spec_data in temp_pro_specification:
            spectitle = spec_data['specTitle']
            final_spec_data = spec_data['specifications']
            temp_list = []
            for temp_spec in final_spec_data:
                key = temp_spec['specName']
                value = temp_spec['specValue']
                kk = f"{key} : {value}"
                temp_list.append(kk)
            final_temp_string = " | ".join(temp_list)
            all_dict[spectitle] = final_temp_string
        specificaions = " || ".join([f'{k} : {all_dict[k]}' for k in all_dict])
    except Exception as e:
        specificaions = ''
        print("Error in final_spec_string . . . . . . . . ", e)

    try:
        images = main_json_data['media']['images']
    except:
        images = []

    if images != []:
        count = 0
        for img in images:
            count += 1
            item[f"Image_{count}"] = str(img['url']).replace('<SIZE>', '600')


    item['product_url'] = product_url
    item['product_name'] = product_name
    item['brand_name'] = brand_name
    item['MPN'] = MPN
    item['SKU'] = SKU
    item['MRP'] = MRP
    item['Offer_price'] = offer_price
    item['Unit_of_Measure'] = Unit_of_Measure
    item['variant'] = variant
    item['color'] = ''
    item['star_rating'] = star_rating
    item['reviews_count'] = reviews_count
    item['description'] = description
    item['stock'] = stock
    item['specificaions'] = specificaions

    return JsonResponse(item)
def product_review(request):
    response_json = dict()
    if 'page' not in request.GET:
        page = 1
    else:
        page = request.GET['page']

    try:
        sort_by = request.GET['sort_by']
    except:
        sort_by = 'photoreview'

    if 'photoreview' in sort_by:
        sort_by = 'photoreview'
    elif 'most_helpful' in sort_by:
        sort_by = 'mosthelpfull'
    elif 'new' in sort_by:
        sort_by = 'newest'
    elif 'old' in sort_by:
        sort_by = 'oldest'
    elif 'lowest_rating' in sort_by or 'lowest' in sort_by:
        sort_by = 'lowestrating'
    elif 'highest_rating' in sort_by or 'highest' in sort_by:
        sort_by = 'highestrating'

    startIndex = ((int(page) - 1) * 10) + 1
    if 'item_id' not in request.GET:
        response_json['response'] = "Invalid item id"
        return JsonResponse(response_json)

    itemId = request.GET['item_id']

    url = "https://www.homedepot.com/federation-gateway/graphql?opname=reviews"

    payload = json.dumps({
        "operationName": "reviews",
        "variables": {
            "filters": {
                "isVerifiedPurchase": False,
                "prosCons": None,
                "starRatings": []
            },
            "itemId": itemId,
            "pagesize": "10",
            "recfirstpage": "10",
            "searchTerm": None,
            "sortBy": sort_by,
            "startIndex": startIndex
        },
        "query": "query reviews($itemId: String!, $searchTerm: String, $sortBy: String, $startIndex: Int, $recfirstpage: String, $pagesize: String, $filters: ReviewsFilterInput) {\n  reviews(itemId: $itemId, searchTerm: $searchTerm, sortBy: $sortBy, startIndex: $startIndex, recfirstpage: $recfirstpage, pagesize: $pagesize, filters: $filters) {\n    Results {\n      AuthorId\n      Badges {\n        DIY {\n          BadgeType\n          __typename\n        }\n        top250Contributor {\n          BadgeType\n          __typename\n        }\n        IncentivizedReview {\n          BadgeType\n          __typename\n        }\n        EarlyReviewerIncentive {\n          BadgeType\n          __typename\n        }\n        top1000Contributor {\n          BadgeType\n          __typename\n        }\n        VerifiedPurchaser {\n          BadgeType\n          __typename\n        }\n        __typename\n      }\n      BadgesOrder\n      CampaignId\n      ContextDataValues {\n        Age {\n          Value\n          __typename\n        }\n        VerifiedPurchaser {\n          Value\n          __typename\n        }\n        __typename\n      }\n      ContextDataValuesOrder\n      Id\n      IsRecommended\n      IsSyndicated\n      Photos {\n        Id\n        Sizes {\n          normal {\n            Url\n            __typename\n          }\n          thumbnail {\n            Url\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      ProductId\n      SubmissionTime\n      TagDimensions {\n        Pro {\n          Values\n          __typename\n        }\n        Con {\n          Values\n          __typename\n        }\n        __typename\n      }\n      Title\n      TotalNegativeFeedbackCount\n      TotalPositiveFeedbackCount\n      ClientResponses {\n        Response\n        Date\n        Department\n        __typename\n      }\n      Rating\n      RatingRange\n      ReviewText\n      SecondaryRatings {\n        Quality {\n          Label\n          Value\n          __typename\n        }\n        Value {\n          Label\n          Value\n          __typename\n        }\n        EnergyEfficiency {\n          Label\n          Value\n          __typename\n        }\n        Features {\n          Label\n          Value\n          __typename\n        }\n        Appearance {\n          Label\n          Value\n          __typename\n        }\n        EaseOfInstallation {\n          Label\n          Value\n          __typename\n        }\n        EaseOfUse {\n          Label\n          Value\n          __typename\n        }\n        __typename\n      }\n      SecondaryRatingsOrder\n      SyndicationSource {\n        LogoImageUrl\n        Name\n        __typename\n      }\n      UserNickname\n      UserLocation\n      Videos {\n        VideoId\n        VideoThumbnailUrl\n        VideoUrl\n        __typename\n      }\n      __typename\n    }\n    Includes {\n      Products {\n        store {\n          Id\n          FilteredReviewStatistics {\n            AverageOverallRating\n            TotalReviewCount\n            TotalRecommendedCount\n            RecommendedCount\n            NotRecommendedCount\n            SecondaryRatingsAveragesOrder\n            RatingDistribution {\n              RatingValue\n              Count\n              __typename\n            }\n            ContextDataDistribution {\n              Age {\n                Values {\n                  Value\n                  Count\n                  __typename\n                }\n                __typename\n              }\n              Gender {\n                Values {\n                  Value\n                  Count\n                  __typename\n                }\n                __typename\n              }\n              Expertise {\n                Values {\n                  Value\n                  __typename\n                }\n                __typename\n              }\n              HomeGoodsProfile {\n                Values {\n                  Value\n                  Count\n                  __typename\n                }\n                __typename\n              }\n              VerifiedPurchaser {\n                Values {\n                  Value\n                  Count\n                  __typename\n                }\n                __typename\n              }\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        items {\n          Id\n          FilteredReviewStatistics {\n            AverageOverallRating\n            TotalReviewCount\n            TotalRecommendedCount\n            RecommendedCount\n            NotRecommendedCount\n            SecondaryRatingsAveragesOrder\n            RatingDistribution {\n              RatingValue\n              Count\n              __typename\n            }\n            ContextDataDistribution {\n              Age {\n                Values {\n                  Value\n                  Count\n                  __typename\n                }\n                __typename\n              }\n              Gender {\n                Values {\n                  Value\n                  Count\n                  __typename\n                }\n                __typename\n              }\n              Expertise {\n                Values {\n                  Value\n                  __typename\n                }\n                __typename\n              }\n              HomeGoodsProfile {\n                Values {\n                  Value\n                  Count\n                  __typename\n                }\n                __typename\n              }\n              VerifiedPurchaser {\n                Values {\n                  Value\n                  Count\n                  __typename\n                }\n                __typename\n              }\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    FilterSelected {\n      StarRatings {\n        is5Star\n        is4Star\n        is3Star\n        is2Star\n        is1Star\n        __typename\n      }\n      VerifiedPurchaser\n      SearchText\n      __typename\n    }\n    pagination {\n      previousPage {\n        label\n        isNextPage\n        isPreviousPage\n        isSelectedPage\n        __typename\n      }\n      pages {\n        label\n        isNextPage\n        isPreviousPage\n        isSelectedPage\n        __typename\n      }\n      nextPage {\n        label\n        isNextPage\n        isPreviousPage\n        isSelectedPage\n        __typename\n      }\n      __typename\n    }\n    SortBy {\n      mosthelpfull\n      newest\n      oldest\n      highestrating\n      lowestrating\n      photoreview\n      __typename\n    }\n    TotalResults\n    __typename\n  }\n}\n"
    })

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
        'Apollographql-Client-Name': 'general-merchandise',
        'Apollographql-Client-Version': '0.0.0',
        'Content-Length': '7103',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'X-Api-Cookies': '{"tt_search":"store_topseller_v1","x-user-id":"02065667-2283-ead7-cadc-ca62c75c8dce"}',
        'X-Cloud-Trace-Context': 'ca695e4ceb284061ac175e09038d7aa7/15',
        'X-Experience-Name': 'general-merchandise',
        'X-Hd-Dc': 'origin'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    json_data = response.json()
    results = list()
    try:data = json_data['data']['reviews']['Results']
    except:
        response_json['failure'] = 'please enter valid endpoint or item id'
        return JsonResponse(response_json)
    else:
        for review in data:
            item = dict()
            try:authorId = review['AuthorId']
            except:authorId = None
            try:username = review['UserNickname']
            except:username = None
            try:reviewId = review['Id']
            except:reviewId = None
            try:ProductId = review['ProductId']
            except:ProductId = None
            try:Title = review['Title']
            except:Title = None
            try:ReviewText = review['ReviewText']
            except:ReviewText = None
            try:IsRecommended = review['IsRecommended']
            except:IsRecommended = None
            try:photos = list({'id':img['Id'] ,'url':img['Sizes']['normal']['Url']} for img in review['Photos'])
            except:photos = None
            try:Rating = review['Rating']
            except:Rating = None
            try:SubmissionTime = review['SubmissionTime']
            except:SubmissionTime = None
            try:TotalNegativeFeedbackCount = review['TotalNegativeFeedbackCount']
            except:TotalNegativeFeedbackCount = None
            try:TotalPositiveFeedbackCount = review['TotalPositiveFeedbackCount']
            except:TotalPositiveFeedbackCount = None

            item['authorId'] = authorId
            item['username'] = username
            item['reviewId'] = reviewId
            item['ProductId'] = ProductId
            item['Title'] = Title
            item['ReviewText'] = ReviewText
            item['IsRecommended'] = IsRecommended
            item['photos'] = photos
            item['SubmissionTime'] = SubmissionTime
            item['Rating'] = Rating
            item['SubmissionTime'] = SubmissionTime
            item['TotalNegativeFeedbackCount'] = TotalNegativeFeedbackCount
            item['TotalPositiveFeedbackCount'] = TotalPositiveFeedbackCount

            results.append(item)

    response_json['results'] = results
    return JsonResponse(response_json)

