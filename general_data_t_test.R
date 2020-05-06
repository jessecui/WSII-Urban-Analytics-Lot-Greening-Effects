greened = read.csv("data/processed_data/greened_lots_crimes.csv", header = T)
vacant = read.csv("data/processed_data/vacant_lots_crimes_final.csv", header = T)

# calculate differences before and after
greened["diff_100_nv"] = greened$nonviolent_100_after - greened$nonviolent_100_before
greened["diff_200_nv"] = greened$nonviolent_200_after - greened$nonviolent_200_before
greened["diff_500_nv"] = greened$nonviolent_500_after - greened$nonviolent_500_before
greened["diff_100_v"] = greened$violent_100_after - greened$violent_100_before
greened["diff_200_v"] = greened$violent_200_after - greened$violent_200_before
greened["diff_500_v"] = greened$violent_500_after - greened$violent_500_before
greened["diff_100_t"] = greened$diff_100_nv + greened$diff_100_v
greened["diff_200_t"] = greened$diff_200_nv + greened$diff_200_v
greened["diff_500_t"] = greened$diff_500_nv + greened$diff_500_v

vacant["diff_100_nv"] = vacant$nonviolent_100_after - vacant$nonviolent_100_before
vacant["diff_200_nv"] = vacant$nonviolent_200_after - vacant$nonviolent_200_before
vacant["diff_500_nv"] = vacant$nonviolent_500_after - vacant$nonviolent_500_before
vacant["diff_100_v"] = vacant$violent_100_after - vacant$violent_100_before
vacant["diff_200_v"] = vacant$violent_200_after - vacant$violent_200_before
vacant["diff_500_v"] = vacant$violent_500_after - vacant$violent_500_before
vacant["diff_100_t"] = vacant$diff_100_nv + vacant$diff_100_v
vacant["diff_200_t"] = vacant$diff_200_nv + vacant$diff_200_v
vacant["diff_500_t"] = vacant$diff_500_nv + vacant$diff_500_v

# Total
t.test(greened$diff_100_t, vacant$diff_100_t, paired = FALSE, alternative = "two.sided")
t.test(greened$diff_200_t, vacant$diff_200_t, paired = FALSE, alternative = "two.sided")
t.test(greened$diff_500_t, vacant$diff_500_t, paired = FALSE, alternative = "two.sided")

t.test(greened$diff_100_v, vacant$diff_100_v, paired = FALSE, alternative = "two.sided")
t.test(greened$diff_200_v, vacant$diff_200_v, paired = FALSE, alternative = "two.sided")
t.test(greened$diff_500_v, vacant$diff_500_v, paired = FALSE, alternative = "two.sided")

t.test(greened$diff_100_nv, vacant$diff_100_nv, paired = FALSE, alternative = "two.sided")
t.test(greened$diff_200_nv, vacant$diff_200_nv, paired = FALSE, alternative = "two.sided")
t.test(greened$diff_500_nv, vacant$diff_500_nv, paired = FALSE, alternative = "two.sided")
