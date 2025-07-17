const express = require('express');
const { listBreweries, getBrewery, searchBreweries, autocompleteBreweries, randomBrewery } = require('../controllers/breweryController');

const router = express.Router();

router.get('/', listBreweries);
router.get('/:id', getBrewery);
router.get('/search', searchBreweries);
router.get('/autocomplete', autocompleteBreweries);
router.get('/random', randomBrewery);

module.exports = router;
