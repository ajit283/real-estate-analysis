import * as playwright from 'playwright';
import { createObjectCsvWriter } from 'csv-writer';


async function main() {
	const browser = await playwright.chromium.launch({
		headless: false // setting this to true will not run the UI
	});

	const page = await browser.newPage();

	await page.goto('https://www.immobilienscout24.de/Suche/radius/haus-kaufen?centerofsearchaddress=Frankfurt%20am%20Main;;;1276007004;Hessen;&geocoordinates=50.11089;8.67949;50.0&enteredFrom=one_step_search');

	let results = []

	await page.waitForTimeout(20000); // wait for 10 seconds to allow manual captcha solving

	// const captcha_button = await page.locator('img').locate('./captcha_button.png').click() // this doesnt work


	await page.locator('css=[data-testid="uc-accept-all-button"]').click() // accept cookies

	let nextpage = await page.locator('css=a[aria-label="Next page"]')

	do {


		const listings = await page.locator('css=.result-list-entry__data')

		console.log(await listings.count())



		for (const listing of await listings.all()) {

			if (await listing.locator('css=a[data-go-to-expose-id]').count() > 0) {

				let id = await listing.locator('css=a[data-go-to-expose-id]').first().getAttribute('data-go-to-expose-id')



				let price = await listing.locator('css=.result-list-entry__primary-criterion:first-child dd')

				console.log(await price.textContent())


				let living_area = listing.locator('css=.result-list-entry__primary-criterion:nth-child(2) dd')

				console.log(await living_area.textContent())

				let location = listing.locator('css=.result-list-entry__map-link')

				console.log(await location.textContent())


				results.push({ id: id, price: await price.textContent(), living_area: await living_area.textContent(), location: await location.textContent() })

			}


		}

		nextpage = await page.locator('css=a[aria-label="Next page"]')


		await nextpage.click()

	} while (await nextpage.getAttribute('tabindex') != -1)

	await browser.close();

	const currentDate = new Date();

	// Get the day, month, and year components of the current date
	const day = String(currentDate.getDate()).padStart(2, '0');
	const month = String(currentDate.getMonth() + 1).padStart(2, '0');
	const year = String(currentDate.getFullYear()).slice(-2);

	// Format the date as DDMMYY
	const formattedDate = `${day}${month}${year}`;


	const csvWriter = createObjectCsvWriter({
		path: `./data/data_${formattedDate}.csv`,
		header: [
			{ id: 'id', title: 'ID' },
			{ id: 'price', title: 'PRICE' },
			{ id: 'living_area', title: 'LIVING_AREA' },
			{ id: 'location', title: 'LOCATION' },
		]
	});

	// Write the data to the CSV file
	await csvWriter.writeRecords(results)


}

main();