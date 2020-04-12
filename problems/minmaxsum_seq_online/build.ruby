check_file = ENV["OTOG_PROBLEM_DIR"] + "/check.cpp"
submit_file = ENV["OTOG_SUBMIT_FILE"]
# puts("[RUBY] ", ENV["OTOG_CLI_DEFINE"])
# puts("[ENV] ", ENV.to_h)
concat_source = (["#include <climits>\n#include <string>\n#include <tuple>\n"] + open(submit_file).to_a + ["\n\n"] + open(check_file).to_a).join('')
concat_file   = ENV["OTOG_CACHE_DIR"] + "/mmsum_seq.cpp"
File.open(concat_file, 'w') { 
  |file| file.write(concat_source)
}
system("g++ -std=c++17 -O2 \"#{concat_file}\" -DOTOG_SERVER $OTOG_CLI_DEFINE -o \"$OTOG_OUT_PROG_FILE\"")
exitstatus = $?.exitstatus
exit(exitstatus)