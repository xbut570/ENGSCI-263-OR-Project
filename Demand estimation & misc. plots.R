#### 263 Test ####

demands = read.csv("WoolworthsDemands.csv")
distances = read.csv("WoolworthsDistances.csv")
locations = read.csv("WoolworthsLocations.csv")
durations = read.csv("WoolworthsTravelDurations.csv")


library(sf)
library(tmap)
library(tidyverse)
library(ggplot2)

locations.sf = st_as_sf(locations, coords = c("Long", "Lat"), crs = 4326)
locations.sf = st_transform(locations.sf, crs = 2193)
locations.demands = left_join(locations.sf, demands, by = c("Store" = "ï..Store"))



locations.demands = locations.demands %>% rowwise() %>% mutate(s = mean(c(X2021.06.14, X2021.06.15, X2021.06.16, 
                                                              X2021.06.17, X2021.06.18, X2021.06.19,
                                                                           X2021.06.21, X2021.06.22, 
                                                              X2021.06.23, X2021.06.24, X2021.06.25,
                                                              X2021.06.26,              X2021.06.28, 
                                                              X2021.06.29, X2021.06.30, X2021.07.01, 
                                                              X2021.07.02, X2021.07.03, 
                                                              X2021.07.05, X2021.07.06, X2021.07.07, 
                                                              X2021.07.08, X2021.07.09, X2021.07.10
                                                                          )))

tmap_mode("view")

tm_shape(locations.demands)+tm_dots(col = "s", size=0.2)

max(locations.demands[["s"]], na.rm = TRUE)
min(locations.demands[["s"]], na.rm = TRUE)
mean(locations.demands[["s"]], na.rm = TRUE)
median(locations.demands[["s"]], na.rm = TRUE)

boxplot(locations.demands[["s"]])



locations.monday = locations.demands %>% rowwise() %>% mutate(s = mean(c(X2021.06.14, X2021.06.21,X2021.06.28, X2021.07.05)))
locations.tuesday = locations.demands %>% rowwise() %>% mutate(s = mean(c(X2021.06.15, X2021.06.22,X2021.06.29, X2021.07.06)))
locations.wednesday = locations.demands %>% rowwise() %>% mutate(s = mean(c(X2021.06.16, X2021.06.23,X2021.06.30, X2021.07.07)))
locations.thursday = locations.demands %>% rowwise() %>% mutate(s = mean(c(X2021.06.17, X2021.06.24,X2021.07.01, X2021.07.08)))
locations.friday = locations.demands %>% rowwise() %>% mutate(s = mean(c(X2021.06.18, X2021.06.25,X2021.07.02, X2021.07.09)))
locations.saturday = locations.demands %>% rowwise() %>% mutate(s = mean(c(X2021.06.19, X2021.06.26,X2021.07.03, X2021.07.10)))

max.weekday.demand = c()
for (i in 1:66){
  max.weekday.demand = c(max.weekday.demand, ceiling(max(c(locations.monday["s"][[1]][i], locations.tuesday["s"][[1]][i], locations.thursday["s"][[1]][i], locations.friday["s"][[1]][i], locations.wednesday["s"][[1]][i]))))
}


boxplot(locations.tuesday[["s"]]  )
boxplot(locations.wednesday[["s"]])
boxplot(locations.thursday[["s"]] )
boxplot(locations.friday[["s"]]   )
boxplot(locations.saturday[["s"]] )



geom_boxplot(locations.monday[["s"]])

tm_shape(locations.tuesday)+tm_dots(col = "s")

test_output = tibble(max.weekday.demand)


test_output = add_column(test_output, saturday = ceiling(locations.saturday["s"][[1]]))
test_output = add_column(test_output, Store = locations.saturday["Store"][[1]])

write.csv(test_output, "Demand by weekday.csv")













