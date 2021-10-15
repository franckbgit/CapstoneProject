/**
 * Get all dealerships
 */



const Cloudant = require('@cloudant/cloudant');

async function main(params) {

	//Connection to the cloudant DB
    const cloudant = Cloudant({
        url: params.COUCH_URL,
        plugins: { iamauth: { iamApiKey: params.IAM_API_KEY } }
    });

	if (params.dealerID) {
		//returns the dealerships with this DealerID

		try {

			let dealerships = await cloudant.db.use('dealerships').find({ "selector": { "id": parseInt(params.dealerID) } })
			dealershipsFormatted = dealerships.docs
			return { dealershipsFormatted };
		
		} catch (error) {
			return { error: error.description };
		}
	}
	else if (params.state) {

		//returns dealership for a specific state

		try {

			let dealerships = await cloudant.db.use('dealerships').find({ "selector": { "st":params.state } })
			dealershipsFormatted = dealerships.docs
			return { dealershipsFormatted };
		
		} catch (error) {
			return { error: error.description };
		}

	}
	else{
		//returns all dealerships

		try {
			
			let dealerships = await cloudant.db.use('dealerships').list({include_docs:true})
			
			let dealershipsFormatted = []
			
			dealerships.rows.forEach((dealership) => { dealershipsFormatted.push(dealership.doc) } )
	
			return {dealershipsFormatted };
		
		} catch (error) {
			return { error: error.description };
		}

	}

}
