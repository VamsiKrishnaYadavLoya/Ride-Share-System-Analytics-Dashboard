This folder codtains my work for Sprint 5 - Poission Regreesion Analysis
The Poisson regression predicts the expected count of an event. Since I am  using it for binary classification (0 or 1), the predicted values will be probabilities. These probabilities will be between 0 and 1, representing the likelihood of the event occurring. 

Feature: Season -> Fall,Spring,Summer,Winter
Output:
poisson regression's rmse value
0.6498363026876407
PR train r2 and rmse
0.6206216477419998
PR test r2 and rmse
Optimization terminated successfully.
         Current function value: 0.839196
         Iterations 4

************
0.18146967366696876

Feature: distance
poisson regression's rmse value
0.47357049534293666
PR train r2 and rmse
0.47357991294480567
PR test r2 and rmse
Optimization terminated successfully.
         Current function value: 0.825330
         Iterations 21

************
0.6007634868976183

Feature: Duration(in Minutes)
poisson regression's rmse value
0.6498363026876407
PR train r2 and rmse
0.621710253552746
PR test r2 and rmse
Optimization terminated successfully.
         Current function value: 0.838181
         Iterations 4

************
0.1715606361311433

Total number of rows Predictions ran:
transportation
bike        20723
escooter    20723
Name: count, dtype: int64
(41446, 10)
